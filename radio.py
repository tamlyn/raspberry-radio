import subprocess
import os
import time
import RPi.GPIO as GPIO

RADIO_PIN1 = 11
RADIO_PIN2 = 12
RADIO_PIN3 = 15
TOGGLE_PIN = 16

PLAYLISTS = [
	'http://www.bbc.co.uk/radio/listen/live/r4_aaclca.pls',
	'http://www.bbc.co.uk/radio/listen/live/r6_aaclca.pls',
	'http://media.kcrw.com/live/kcrwmusic.pls'
]

def main():
	GPIO.setup(RADIO_PIN1, GPIO.IN)
	GPIO.setup(RADIO_PIN2, GPIO.IN)
	GPIO.setup(RADIO_PIN3, GPIO.IN)
	GPIO.setup(TOGGLE_PIN, GPIO.IN)
	
	mplayerBaseArgs = ['mplayer', '-softvol', '-cache', '256', '-afm', 'mp3lib', '-quiet', '-playlist']
	shairportArgs = ['perl', '/usr/local/bin/shairport.pl']
	mode = 0
	pid = None
	
	print "Started. Waiting for GPIO input."
	
	while 1:
		oldMode = mode
		
		if (not GPIO.input(TOGGLE_PIN)):
			mode = 4 #airplay
		elif (not GPIO.input(RADIO_PIN1)):
			mode = 1 #mplayer
		elif (not GPIO.input(RADIO_PIN2)):
			mode = 2 #mplayer
		elif (not GPIO.input(RADIO_PIN3)): 
			mode = 3 #mplayer
		else:
			mode = 0 #stopped
	
		#mode has changed
		if (oldMode != mode):
			print 'Mode changed'
			#kill old process, if any
			if (pid):
				os.kill(pid, 15)
				print "Killing process " + str(pid)
			
			if (mode == 4):
				args = shairportArgs
				print "Starting ShairPort"
			elif (mode == 0):
				print "Stopped"
				continue
			elif (0 < mode < 4):
				args = mplayerBaseArgs + [PLAYLISTS[mode-1]]
				print "Playing " + PLAYLISTS[mode-1]
			
			pid = subprocess.Popen(args).pid
			
		#sleep for a short time
		time.sleep(0.5)
	
	
if __name__ == '__main__':
	main()
