from subprocess import call
import os.path as pathCheck
import os

class wirelessSocket(object):
	_send_path = "/home/pi/raspberry-remote/send" # path to send file from raspberry-remote
	_settings_path = "/var/www/heimautomation/settings/" # path to settings dir
	_steckdosen_codes = {}

	#constructor
	def __init__(self):
		# define the socket codes
		self._steckdosen_codes['lichtBett'] = ['00111','1'] # [homecode, socket number]
		self._steckdosen_codes['tvbox'] = ['01111','1']
		self._steckdosen_codes['tv'] = ['01111','2']

	# sends the wireless socket code and status
	def __send(self, steckdose, status):
		call([self._send_path, self._steckdosen_codes[steckdose][0], self._steckdosen_codes[steckdose][1],str(status)])
		# creates the settingsfile for other tools and check for isActive
		if(status == 1):
			file = open(self._settings_path+steckdose+'.info', 'w+') # create info fille (socket on)
			file.close()
		else:
			os.remove(self._settings_path+steckdose+'.info') # remove info file (socket off)

	# check if info file exists
	def __checkStatus(self, steckdose):
		return pathCheck.isfile(self._settings_path+steckdose+'.info')

	def schalten(self, steckdose):
		status = 1 # socket on
		# if socket on
		if(self.__checkStatus(steckdose)):
			status = 0 # socket off
		self.__send(steckdose, status)
