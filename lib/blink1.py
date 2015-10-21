from subprocess import call
import os.path as pathCheck
from time import sleep
import os
import random

class blink1(object):
	def on(self):
		call(['blink1-tool','--on'])

	def off(self):
		call(['blink1-tool','--off'])

	def policeAlarm(self, counter):
		for i in range(counter):
			call(['blink1-tool','--red','--led=1','--millis=0','--delay=0'])
			call(['blink1-tool','--blue','--led=2','--millis=0','--delay=0'])
			sleep(0.05)
			call(['blink1-tool','--red','--led=2','--millis=0','--delay=0'])
			call(['blink1-tool','--blue','--led=1','--millis=0','--delay=0'])
			sleep(0.05)

	def plentFarm(self,zeit=30):
		call(['blink1-tool','--green','--millis=0','--delay=0'])
		call(['blink1-tool','--yellow','--millis='+str(zeit*1000),'--delay='+str(zeit*1000)])
		sleep(zeit)
		call(['blink1-tool','--red','--millis='+str(zeit*1000),'--delay='+str(zeit*1000)])
		sleep(zeit)

	def setRgbColor(self,rgb,led=0,millis=300,delay=300):
		call(['blink1-tool','--rgb='+rgb,'--led='+str(led), '--millis='+str(millis),'--delay='+str(delay)])

	def setHsbColor(self,farbton,saettigung=1,helligkkeit=255, led=0):
		call(['blink1-tool','--hsb='+str(farbton)+','+str(saettigung)+','+str(helligkkeit),'--led='+str(led)])

	def strobe(self,repeats=200):
		call(['blink1-tool', '--flash='+str(repeats),'--millis=0', '--delay=10','--verbose'])

	def defuseStrobe(self,repeats=200):
		for i in range(repeats):
			delay = random.randint(20,100)
			call(['blink1-tool', '--flash='+str(10),'--millis=0', '--delay='+str(delay),'--verbose'])
			sleep(delay/1000)
