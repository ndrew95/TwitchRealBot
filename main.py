#!/usr/bin/env python
'# -- coding: utf-8 --' 
import socket, string
import requests
import json
import html
import time
import re
import urllib
import datetime
import sys
import os
from random import *
import datetime
import random
import gc

# Set all the variables necessary to connect to Twitch IRC
HOST = 'irc.twitch.tv'
NICK = b'[YOURINFO]'
PORT = 6667
PASS = b'[YOURINFO]'
readbuffer = b''
MODT = False

messageCount = 0
messageCountSub = 0
wordsusedString = ''
wordsusedStringBetter = ''
messagesList = []
lastMessage = []

#Connect to the Twitch servers.
s = socket.socket()
s.connect((HOST, PORT))
s.send(b'PASS ' + PASS + b'\r\n')
s.send(b'NICK ' + NICK + b'\r\n')
s.send(b'JOIN #[CHANNEL NAME] \r\n')

#This function allows the script to send a message to the chat.
def Send_message(message):
	s.send((("""PRIVMSG #[CHANNEL NAME] :  %s  \r\n""")%(message)).encode('utf-8'))


while True:
	botPause = time.time() + 60

	#try-except statement to ensure a memory leak is not caused by ongoing running of this script.
	try:
		chatAppend.close()
		chatRead.close()
		randNumbz.close()
		randNumbzx.close()
		del wordsusedStringBetter
		wordsusedStringBetter = ''

		gc.collect()
	
	except:
		wordsusedStringBetter = ''

		gc.collect()
	
	readbuffer = readbuffer+ s.recv(1024)
	temp = readbuffer.split(b'\n')

	readbuffer = temp.pop()

	messageCount = messageCount+1
	messageCountSub = messageCountSub + 1

	for line in temp:
		del wordsusedStringBetter
		wordsusedStringBetter = ''
		gc.collect()
		
		#Pings Twitch's API so the bot does not get disconnected by Twitch
		if time.time() > disconnectTime:
			s.send(b'PING :tmi.twitch.tv\r\n')
			disconnectTime = time.time() + 60*3
			
		# Checks whether the message is PING because its a method of Twitch to check if you're afk
		if b'PING :tmi.twitch.tv' in line:
			print('PONG :tmi.twitch.tv')
			s.send(b'PONG :tmi.twitch.tv\r\n')
			

		else:

			if 'QUIT' not in parts[1] and 'JOIN' not in parts[1] and 'PART' not in parts[1]:
				try:
					message = parts[2][:len(parts[2]) - 1]
				except:
					message = ''

				# Sets the username variable to the actual username
				usernamesplit = str(parts[1]).split('!')
				username = usernamesplit[0]

				# Only works after twitch is done announcing stuff (MODT = Message of the day)
				if MODT:
					
					randNumb=randint(1,99999)

					chatAppend=open('dataChat2.txt', 'a+')
					chatRead=open('dataChat2.txt', 'r')

					wordsused = chatRead.readlines()
					listwords = chatAppend.read()
					randNumbz=open('commonChat.txt', 'a+')

					#append all messages to a txt file
					randNumbz.write(str(message).replace('\\r','') + '. ')
					randNumbzx=open('commonChat.txt', 'r')


					#create a list of the most recent messages
					keywordstest = message.split(' ')

					#iterate through most recent messages, remove redudant messages
					for i in keywordstest:
						if keywordstest.count(i)>1:
							while keywordstest.count(i)>1:
								keywordstest.remove(i)

					#do not include common words
					stopWords = ['tmi.twitch.tv\\r','What','yeah','ya','u','you','like','gave','I','i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now']
					
					#iterate through non-redudant messages
					for i in keywordstest:

						#if the message isn't redudant, and not a common word, check it
						if i in messagesList and i not in stopWords:

							#if a similar message has been sent at least 3 times in the span of a minute, move forward.
							if messagesList.count(i)>=3:
								keywordTest = i
								keywordTest = keywordTest.replace('\\r','')
								wordCount=3
								del messagesList[:]
								messagesList = []
							

						messagesList.append(i)
					
	
					#if a similar message has been sent at least three times, try to find a similar message, and send it to the chat.
					if wordCount>= 3 and time.time() > botPause:

						#if similar messages are being sent, but the keyword does not exist in the file, break the loop.
						wordNotExist = wordsusedString.find(keywordTest.rstrip())
						if wordNotExist ==-1:
							wordCount = 0
							break

						#if the keyword exists, search for a sentence that contains the keyword.
						else:
							sendWord = re.search(r'([^.]*?(\b%s\b).*?\.)(?!\d)' % keywordTest,wordsusedStringBetter)

							#if the sentence has already been sent too the chat, do not send it. Furthermore, remove it from the last message list.
							if sendWord.groups()[0] in lastMessage:
								del lastMessage[:]
								lastMessage = []
								break

							#if the sentence has not been sent, send the message, and add the message to the list, so it cannot be sent twice.
							else:
								Send_message(sendWord.groups()[0])
								lastMessage.append(sendWord.groups()[0])
								os.execv(sys.executable, [sys.executable] + sys.argv)
								wordsusedStringBetter = ''
					
						#pause the bot for a minute so it doesn't spam messages, if similar messages are being sent.
						botPause = time.time() + 60
						wordCount = 0

					#if a message isn't sent by the bot, append what message it sees to the file to be referenced later.
					else:
						chatAppend.write(str(message).replace('\\r', '') + '. ')
				

					chatAppend.close()
					chatRead.close()
					randNumbz.close()
					randNumbzx.close()


				for l in parts:
					if 'End of /NAMES list' in l:
						MODT = True

	chatAppend.close()
	chatRead.close()
	f.close()
	xy.close()
	randNumbz.close()
	randNumbzx.close()
