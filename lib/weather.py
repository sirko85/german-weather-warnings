def module_exists(module_name):
	try:
		__import__(module_name)
	except ImportError:
		return False
	else:
		return True

import doctest
import datetime
from datetime import datetime
import ftplib
import zipfile
import glob
import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
import xml.etree.ElementTree as ET
from subprocess import call
if(module_exists('lib.blink1')):
	from lib.blink1 import blink1
if(module_exists('RPi.GPIO')):
	import RPi.GPIO as GPIO
if(module_exists('smtplib')):
	import smtplib
	from email.mime.text import MIMEText

class weather(object):

	__configPath = 'config'

	def __init__(self):
		config = __import__(self.__configPath)
		self.__ftp_user = config.ftp_user
		self.__ftp_password = config.ftp_password
		self.__ftp_server = config.ftp_server
		self.__location_id = config.location_id
		self.__download_dir = config.download_dir
		self.__notifications = config.notifications
		self.__db = sqlite3.connect('weather.db')
		self.__db.row_factory = sqlite3.Row
		#from lib.blink1 import blink1
		#self.blink1 = __import__('lib.blink1')

	def updateWeatherWarnings(self):
		self.__connectFtp()
		self.__downloadWeatherWarnings()
		self.__importWeatherWarnings()

		cursor = self.__db.cursor()
		sql_command = """UPDATE checks SET created_at = {created_at}"""
		sql_command = sql_command.format(created_at="(datetime('now','localtime'))")
		cursor.execute(sql_command)
		self.__db.commit()

	def __connectFtp(self):
		"""
			Connect to FTP Server
		>>> x = weather()
		>>> x.downloadNewFiles()
		True
		True
		"""
		self.__dwd_ftp = ftplib.FTP(self.__ftp_server)
		self.__dwd_ftp.login(self.__ftp_user, self.__ftp_password)
		return True

	def __downloadWeatherWarnings(self):
		"""
			load all weatherwarnings from today
			TODO load all weatherwarnings since last download
		"""
		directory = '/gds/gds/specials/alerts/cap/GER/status/'
		self.__dwd_ftp.cwd(directory)

		cursor = self.__db.cursor()
		sql_command = """SELECT created_at FROM checks ORDER BY created_at DESC LIMIT 1"""
		cursor.execute(sql_command)
		res = cursor.fetchone()
		if(res is None):
			print('No date found... starting download from today 00 o\'Clock.')
			sql_command = """INSERT INTO checks(created_at) VALUES ({created_at})"""
			sql_command = sql_command.format(created_at="(datetime('now','localtime'))")
			cursor.execute(sql_command)
			self.__db.commit()
			current_time = datetime.today()
			current_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
		else:
			current_time = datetime.strptime(res[0],'%Y-%m-%d %H:%M:%S')

		tag = current_time.day
		if(tag < 10):
			tag = '0' + str(tag)

		stunde = current_time.hour
		if(stunde < 10):
			stunde = '0' + str(stunde)

		minute = current_time.minute
		if(minute < 10):
			minute = '0' + str(minute)

		current_day = str(current_time.year) + str(current_time.month) + str(tag) + str(stunde) + str(minute)
		filenames = self.__dwd_ftp.nlst()
		filenames.sort(reverse=True)
		for filename in filenames:
			current_file_time = datetime.strptime(filename[13:25],'%Y%m%d%H%M%S')
			if(current_file_time <= current_time):
				continue

			print('"'+filename+ '" downloaded.')
			file = open(self.__download_dir + filename, 'wb')
			self.__dwd_ftp.retrbinary('RETR ' + filename, file.write)
			file.close()
			with zipfile.ZipFile(self.__download_dir + filename) as zf:
				zf.extractall(self.__download_dir)

			os.remove(self.__download_dir + filename)

		self.__dwd_ftp.close()
		return True

	def __importWeatherWarnings(self):
		os.chdir(self.__download_dir)
		files = glob.glob("*.xml")
		files.sort()
		cursor = self.__db.cursor()
		for file in files:
			fileObject = open(file).read()
			has_location_id = False
			# TODO Make it better!
			for current_location_id in self.__location_id:
				if current_location_id in fileObject:
					has_location_id = True

			if not has_location_id:
				os.remove(file)
				continue

			alert = ET.parse(file)
			root = alert.getroot()
			msgType = root.find('{urn:oasis:names:tc:emergency:cap:1.2}msgType').text
			info = root.find('{urn:oasis:names:tc:emergency:cap:1.2}info')
			weather_group = ''
			area_color = ''
			for child in info.findall('{urn:oasis:names:tc:emergency:cap:1.2}eventCode'):
				if(child.find('{urn:oasis:names:tc:emergency:cap:1.2}valueName').text == 'GROUP'):
					weather_group = child.find('{urn:oasis:names:tc:emergency:cap:1.2}value').text

				if(child.find('{urn:oasis:names:tc:emergency:cap:1.2}valueName').text == 'AREA_COLOR'):
					area_color = child.find('{urn:oasis:names:tc:emergency:cap:1.2}value').text

			event = info.find('{urn:oasis:names:tc:emergency:cap:1.2}event').text
			expires = datetime.strptime(info.find('{urn:oasis:names:tc:emergency:cap:1.2}expires').text,'%Y-%m-%dT%H:%M:%S+00:00')
			onset = datetime.strptime(info.find('{urn:oasis:names:tc:emergency:cap:1.2}onset').text,'%Y-%m-%dT%H:%M:%S+00:00')
			headline = info.find('{urn:oasis:names:tc:emergency:cap:1.2}headline').text
			description = info.find('{urn:oasis:names:tc:emergency:cap:1.2}description').text
			sql_command = """INSERT OR IGNORE INTO weather_warnings (msgType, event, weather_group, color, headline, description, created_at, valid_from, valid_till)
				VALUES ('{msgType}', '{event}', '{weather_group}', '{color}', '{headline}', '{description}', {created_at}, "{valid_from}", "{valid_till}")"""
			sql_command = sql_command.format(msgType=msgType,event=event, weather_group=weather_group,color=area_color,headline=headline, description=description, created_at="(datetime('now','localtime'))", valid_from=onset, valid_till=expires)
			cursor.execute(sql_command)
			self.__db.commit()
			os.remove(file)
		return True

	def __getLocationIds(self):
		os.chdir(self.__download_dir)
		files = glob.glob("*.xml")
		files.sort()
		cursor = self.__db.cursor()
		areas = {}

		for file in files:
			alert = ET.parse(file)
			root = alert.getroot()
			info = root.find('{urn:oasis:names:tc:emergency:cap:1.2}info')
			if info is None:
				continue

			for child in info.findall('{urn:oasis:names:tc:emergency:cap:1.2}area'):
				for child2 in child.findall('{urn:oasis:names:tc:emergency:cap:1.2}geocode'):
					if(child2.find('{urn:oasis:names:tc:emergency:cap:1.2}valueName').text == 'WARNCELLID'):
						cellid = child2.find('{urn:oasis:names:tc:emergency:cap:1.2}value').text
				areaDesc = child.find('{urn:oasis:names:tc:emergency:cap:1.2}areaDesc').text
				areas[cellid] = areaDesc
			os.remove(file)
		return areas


	def activateNotification(self, res):
		"""
		Activate the notification. Configuration for notifications is in the config.py.
		>>> x = weather()
		>>> x.activateNotification()
		True
		"""
		newRgb = ''
		for current_color in res[0]["color"].split():
			temp = hex(int(current_color))
			temp = str(temp)[-2:]
			if(temp == 'x0'):
				temp = '00'
			newRgb += temp

		try:
			if(self.__notifications['blink1']['status'] == 'on'):
				signal = blink1()
				signal.setRgbColor(newRgb)
				signal.strobe()
		except:
			print('Error for blink(1)')
		try:
			if(self.__notifications['raspberry']['status'] == 'on'):
				GPIO.cleanup()
				GPIO.setmode(GPIO.BOARD)
				GPIO.setup(self.__notification['raspberry']['gpiopin'], GPIO.OUT)
				GPIO.output(self.__notification['raspberry']['gpiopin'], True)
		except:
			print('Error for raspberry')
		try:
			if(self.__notifications['telegram']['status'] == 'on'):
				self.__sendTelegram(res)
		except:
			print('Error for telegram')
		try:
			if(self.__notifications['mail']['status'] == 'on'):
				self.__sendMail(res)
		except:
			print('Error for E-Mail')
		return True

	def __sendTelegram(self,res):
		for currentRes in res:
			msg = self.__notifications['telegram']['msg']
			msg = msg.format(headline=currentRes['headline'],description=currentRes['description'],valid_till=currentRes['valid_till'])
			call(self.__notifications['telegram']['telegram_path'], 'msg='+msg, 'fwd='+self.__notifications['telegram']['contactname'])
			if(self.__notifications['mail']['automaticcheck']):
				self.setStatusChecked(currentRes)
		return True

	def __sendMail(self,res):
		msg = ''
		for currentRes in res:
			msgPart = self.__notifications['mail']['msg']
			msgPart = msgPart.format(headline=currentRes['headline'],description=currentRes['description'],valid_till=currentRes['valid_till'],valid_from=currentRes['valid_from'], color=currentRes['color'], weather_group=currentRes['weather_group'], event=currentRes['event'], msgType=currentRes['msgType'])
			msg = msg + msgPart
		msg = MIMEText(msg)

		# me == the sender's email address
		# you == the recipient's email address
		msg['Subject'] = self.__notifications['mail']['subject']
		msg['From'] = self.__notifications['mail']['mail']
		msg['To'] = self.__notifications['mail']['mail']

		# Send the message via our own SMTP server.
		s = smtplib.SMTP('localhost')
		s.send_message(msg)
		s.quit()
		if(self.__notifications['mail']['automaticcheck']):
			self.setStatusChecked()
		return True

	def deactivateNotification(self):
		"""
		TODO Deactivate signal.
		>>> x = weather()
		>>> x.deactivateNotification()
		True
		"""
		return True

	def checkWeatherWarnings(self):
		"""
		search for not checked warnings and activate notification.
		>>> weather.setStatusChecked()
		True
		"""

		cursor = self.__db.cursor()
		sql_command = """SELECT * FROM weather_warnings WHERE valid_till >= (datetime('now','localtime')) AND is_checked = 'False' ORDER BY msgType"""
		cursor.execute(sql_command)
		res = cursor.fetchall()
		if(len(res) == 0):
			return False
		self.activateNotification(res)
		return True

	def setStatusChecked(self,currentRes = None):
		"""
		Set current warning on checked
		>>> weather.setStatusChecked()
		True
		"""
		cursor = self.__db.cursor()
		if(currentRes is not None):
			sql_command = """UPDATE weather_warnings SET is_checked = 'True' WHERE is_checked = 'False' AND rowid = {id}"""
			sql_command = sql_command.format(id=currentRes['rowid'])
			cursor.execute(sql_command)
			self.__db.commit()
			return True

		sql_command = """SELECT rowid FROM weather_warnings WHERE valid_till >= (datetime('now','localtime')) AND is_checked = 'False' ORDER BY msgType"""
		cursor.execute(sql_command)
		res = cursor.fetchone()
		if(res is None):
			return False
		sql_command = """UPDATE weather_warnings SET is_checked = 'True' WHERE is_checked = 'False' AND rowid = {id}"""
		sql_command = sql_command.format(id=res['rowid'])
		cursor.execute(sql_command)
		self.__db.commit()
		return True

	def printCurrentIds(self):
		self.__connectFtp()
		self.__downloadWeatherWarnings()
		areas = self.__getLocationIds()
		for cellid, areaDesc in areas.items():
			print(str(cellid) + ': ' + areaDesc)

if __name__ == "__main__":
	doctest.testmod()
