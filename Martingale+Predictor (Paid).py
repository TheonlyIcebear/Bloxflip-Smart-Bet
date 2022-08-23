#!/usr/bin/env python -W ignore::DeprecationWarning 

import cloudscraper, subprocess, threading, requests, logging, base64, json, time, os
from websocket import create_connection
from win10toast import ToastNotifier
from playsound import playsound
from random import randbytes
from termcolor import cprint
from zipfile import *
from sys import exit



class main:
	def __init__(self):
		logging.basicConfig(filename="errors.txt", level=logging.DEBUG)
		self.crashPoints = None
		self.multiplier = 0
		self.version = "1.3"
		os.system("")
		try:
			self.getConfig()
			self.sendBets()
		except KeyboardInterrupt:
			self.print("Exiting program.")
			
			exit()
		except Exception as e:
			open("errors.txt", "w+").close()
			now = time.localtime()
			logging.exception(f'A error has occured at {time.strftime("%H:%M:%S %I", now)}')
			self.print("An error has occured check logs.txt for more info", "error")
			time.sleep(2)
			raise e

	def print(self, message="", option=None): # print the ui's text with
		print("[ ", end="")
		if not option:
			cprint("AUTOBET", "magenta", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "magenta")
		elif option == "error":
			cprint("ERROR", "red", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "red")
		elif option == "warning":
			cprint("WARNING", "yellow", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "yellow")
		elif option == "yellow":
			cprint("AUTOBET", "yellow", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "yellow")
		elif option == "good":
			cprint("AUTOBET", "green", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "green")
		elif option == "bad":
			cprint("AUTOBET", "red", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "red")

	def sendwbmsg(self,url,message,title,color,content):
		if "https://" in url:
			data = {
				"content": content,
				"username": "Smart Bet",
				"embeds": [
									{
										"description" : message,
										"title" : title,
										"color" : color
									}
								]
			}
			r = requests.post(url, json=data)

	def clear(self): # Clear the console
		os.system('cls' if os.name == 'nt' else 'clear')


	def getBalance(self):
		uiprint = self.print
		balance = None

		scraper = cloudscraper.create_scraper()
		try: 
			balance = scraper.get("https://rest-bf.blox.land/user", headers={
						"x-auth-token": self.auth
				}).json()["user"]["wallet"]
		except Exception as e:
			uiprint("Invalid authorization. Make sure you copied it correctly, and for more info check the github", "bad")
			time.sleep(1.7)
			exit()
		return round(balance, 2)

	def Connect(self):
		return create_connection("wss://sio-bf.blox.land/socket.io/?EIO=3&transport=websocket",
								suppress_origin=True, 
								header={
										"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
										"Accept": "*/*",
										"Accept-Language": "en-US,en;q=0.5",
										"Accept-Encoding": "gzip, deflate, br",
										"Sec-WebSocket-Version": "13",
										"Origin": "https://www.piesocket.com",
										"Sec-WebSocket-Extensions": "permessage-deflate",
										"Sec-WebSocket-Key": "0x5NztKGVafNhIXjearNdg==",
										"Connection": "keep-alive, Upgrade",
										"Sec-Fetch-Dest": "websocket",
										"Sec-Fetch-Mode": "websocket",
										"Sec-Fetch-Site": "cross-site",
										"Pragma": "no-cache",
										"Cache-Control": "no-cache",
										"Upgrade": "websocket"
				}
			)

	def getConfig(self): # Get configuration from config.json file
		uiprint = self.print
		print("[", end="")
		cprint(base64.b64decode(b'IENSRURJVFMg').decode('utf-8'), "cyan", end="")
		print("]", end="")
		print(base64.b64decode(b'IE1hZGUgYnkgSWNlIEJlYXIjMDE2NyAmIEN1dGVjYXQgYnV0IHRlcm1lZCM0NzI4').decode('utf-8'))
		time.sleep(3)
		self.clear()

		try:
			open("config.json", "r").close()
		except:
			uiprint("config.json file is missing. Make sure you downloaded all the files and they're all in the same folder", "error")

		with open("config.json", "r+") as data:
			try:
				config = json.load(data)
				self.multiplier = float(config["multiplier"])
				if self.multiplier < 2:
					uiprint("Multiplier must be above 2 to make profit.", "error")
					time.sleep(1.6)
					exit()
			except ValueError as e:
				uiprint("Invalid multiplier inside JSON file. Must be valid number", "error")
				time.sleep(1.6)
				exit()

			try:
				self.average = int(config["games_averaged"])
				if self.average > 35:
					uiprint("Too many games_averaged. Must be 35 or less games", "error")
					time.sleep(1.6)
					exit()
			except:
				uiprint("Invalid amount of games to be averaged inside JSON file. Must be valid number", "error")
				time.sleep(1.6)
				exit()


			try:
				self.auth = config["authorization"]
			except:
				uiprint("Invalid authorization inside JSON file. Enter your new authorization from BloxFlip", "error")
				time.sleep(1.6)
				exit()


			try:
				self.key = config["key"]
			except:
				uiprint("Invalid key inside JSON file. Make sure it's a valid string", "error")
				time.sleep(1.6)
				exit()


			try:
				self.disablePredictor = not config["predict_crash"]
			except:
				uiprint("Invalid play_sounds boolean inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				exit()


			try:
				self.martingale = config["martingale"]
			except:
				uiprint("Invalid play_sounds boolean inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				exit()


			try:
				self.sound = config["play_sounds"]
			except:
				uiprint("Invalid play_sounds boolean inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				exit()


			try:
				self.webhook = config["webhook"]
				if not "https://" in self.webhook:
					uiprint("Invalid webhook inside JSON file file. Make sure you put the https:// with it.", "warning")
					self.webhook = None
			except:
				uiprint("Invalid webhook string inside JSON file. Make sure it's a valid string", "error")
				time.sleep(1.6)
				exit()

			try:
				self.betamount = float(config["bet_amount"])
			except:
				uiprint("Invalid bet_amount inside JSON file. Must be valid number", "error")
				time.sleep(1.6)
				exit()


			try:
				self.maxbet =  float(config["max_betamount"])
			except:
				uiprint("Invalid max_betamount amount inside JSON file. Must be a valid number", "error")
				time.sleep(1.6)
				exit()


			try:
				self.skip =  config["skip_losing_streaks"]
			except:
				uiprint("Invalid skip_losing_streaks boolean inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				exit()


			try:
				self.bet = float(config["auto_bet"])
			except:
				uiprint("Invalid bet inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				exit()


			try:
				self.stop =  float(config["auto_stop"])
			except:
				uiprint("Invalid auto_stop amount inside JSON file. Must be a valid number", "error")
				time.sleep(1.6)
				exit()


			try:
				self.stoploss =  float(config["stop_loss"])
			except:
				uiprint("Invalid auto stop_loss inside JSON file. Must be a valid number", "error")
				time.sleep(1.6)
				exit()


			try:
				self.restart = config["auto_restart"]
			except:
				uiprint("Invalid auto_restart boolean inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				exit()

			if not type(self.restart) == bool:
				uiprint("Invalid auto_restart boolean inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				exit()
			self.hwid = current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

			version = self.version
			latest_release = requests.get("https://bfpredictor.repl.co/latest_release").text
			if latest_release == version:
				uiprint("Your version is up to date.", "good")
			else:
				uiprint(f"You are currently on v{version}. Please update to the newest version {latest_release}", "error")
				time.sleep(10)
				exit()


			while True:
				try:
				 	self.ws = self.Connect()
				 	break
				except Exception as e:
				 	uiprint("Failed to connect to webserver. Retrying in 1.5 seconds...", "error")
				 	print(e)
				 	time.sleep(1.5)

			ws = self.ws

			ws.send("40/crash,")
			ws.send(f'42/crash,["auth","{self.auth}"]')


	def ChrashPoints(self):
		average = self.average
		history = None
		uiprint = self.print
		sent = False
		scraper = cloudscraper.create_scraper()

		while True:
			try:
				games = scraper.get("https://rest-bf.blox.land/games/crash", headers={
						"x-auth-token": self.auth
					})
				games.json()
			except:
				continue
			games = games.json()

			if not history == games["history"]:
				history = games["history"]
				yield [games["history"][0]["crashPoint"], [float(crashpoint["crashPoint"]) for crashpoint in history]]
			time.sleep(0.01)


	def ChrashPoints(self):
		average = self.average
		history = None
		uiprint = self.print
		sent = False
		scraper = cloudscraper.create_scraper()

		while True:
			try:
				games = scraper.get("https://rest-bf.blox.land/games/crash", headers={
						"x-auth-token": self.auth
					}).json()
			except:
				continue

			if not history == games["history"]:
				history = games["history"]
				yield [games["history"][0]["crashPoint"], [float(crashpoint["crashPoint"]) for crashpoint in history]]
			time.sleep(0.01)

	def playsounds(self, file):
		if self.sound:
			playsound(file)


	def sendBets(self): # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("Betting started. Press Ctrl + C to exit")

		disablePredictor = self.disablePredictor
		sendwebhookmsg = self.sendwbmsg
		multiplier = self.multiplier
		playsounds = self.playsounds
		martingale = self.martingale
		betamount = self.betamount
		stoploss = self.stoploss
		average = self.average
		restart = self.restart
		webhook = self.webhook
		maxbet = self.maxbet
		stop = self.stop
		skip = self.skip
		lastgame = None
		bet = self.bet
		key = self.key
		winning = 0
		losing = 0

		prediction = multiplier

		for game in self.ChrashPoints():
			uiprint("Game Starting...")
			balance = self.getBalance()

			games = game[1][::-1][-average:]
			pause = True
			accuracy = None
			lastgame = game[0]
			avg = sum(games[-3:])/len(games[-3:])
			streak = [1, 0]
			uiprint(f"Average Crashpoint: {avg}")


			for game in games:
				if game > 2:
					streak[0] += 1
				else:
					streak[1] += 1

			try:
				if lastgame >= prediction:
					if not self.webhook == None:
						sendwebhookmsg(self.webhook, f"You have made {betamount*multiplier - betamount} robux", f"You Won!", 0x83d687, f"")
					accuracy = (1-((lastgame-prediction)/lastgame))*100

					if martingale and not pause:
						betamount = self.betamount
						uiprint(f"Won previous game. lowering bet amount to {betamount}", "good")
					pause = False
					if not disablePredictor:
						uiprint(f"Accuracy on last guess: {accuracy}", "yellow")
					
						
					try:
						threading.Thread(target=playsounds, args=('Assets\Win.mp3',)).start()
					except:
						pass
				else:
					if martingale and not pause:
						betamount *= 2
						uiprint(f"Lost previous game. Increasing bet amount to {betamount}", "bad")
					pause = True
					if not self.webhook == None:
						sendwebhookmsg(self.webhook, f"You lost {betamount} robux\n You have {balance} left", f"You Lost!", 0xcc1c16, f"")
					accuracy = (1-((prediction-lastgame)/lastgame))*100
					if not disablePredictor:
						uiprint(f"Accuracy on previous guess: {accuracy}", "yellow")
					
					try:
						threading.Thread(target=playsounds, args=('Assets\Loss.mp3',)).start()
					except:
						pass
				
			except ValueError:
				uiprint(f"No data for accuracy calculations", "error")
			except TypeError:
				uiprint(f"No data for accuracy calculations", "error")
			except UnboundLocalError:
				uiprint(f"No data for accuracy calculations", "error")
			except NameError:
				uiprint(f"No data for accuracy calculations", "error")


			if streak[0] > streak[1]:
					uiprint("Winning streak detected.", "good")
			else:
				uiprint("Losing streak detected", "bad")
				if skip:
					uiprint("Skipping this round.", "warning")
					continue

			try:
				games[0]
			except:
				continue
			
			if not disablePredictor:
				chance = 1
				for game in games[-2:]:
					chance *= (1 - (1/33 + (32/33)*(.01 + .99*(1 - 1/game))))

				while True:
					request = requests.get("https://bfpredictor.repl.co/multiplier", 
											data={"key": key, 
												  "average": avg,
												  "multiplier": self.multiplier, 
												  "hwid": self.hwid,
												  "chance": chance
											}
										)

					if request.status_code == 403:
						uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/blox", "error")
						input("Press enter to exit >> ")
	
						exit()
					elif request.status_code == 500:
						uiprint("Internal server error. Trying again 1.5 seconds...", "error")
						time.sleep(1.5)
					elif request.status_code == 200:
						prediction = float(request.text)
						break
					else:
						uiprint("Internal server error. Trying again 1.5 seconds...", "error")
						time.sleep(1.5)

				if prediction < 2:
					uiprint(f"Game will likely crash around {prediction}. Ignoring and betting on 2 to ensure profit.")
					prediction = 2


				uiprint(f"Setting multiplier to {prediction}", "yellow")


			
			uiprint(f"Your balance is {balance}")
			if balance < betamount:
				uiprint("You don't have enough robux to continue betting.", "error")
				threading.Thread(target=playsounds, args=('Assets\Loss.mp3',)).start()
				ToastNotifier().show_toast("Bloxflip Smart Bet", 
					   "Oh No! You've run out of robux to bet!", duration = 3,
				 	   icon_path ="assets\\Bloxflip.ico",
				 	   threaded=True
				 	   )
				if not balance < self.betamount and not restart:
					input(f"Press enter to restart betting with {self.betamount} robux")
					betamount = self.betamount
				elif not balance < self.betamount and restart:
					uiprint("Overwritten: Auto Restart is enabled", "warning")
					threading.Thread(target=playsounds, args=('Assets\Win.mp3',)).start()
					ToastNotifier().show_toast("Bloxflip Smart Bet", 
						   "Overwritten: Auto restart is enabled.", duration = 3,
					 	   icon_path ="assets\\Bloxflip.ico",
					 	   threaded=True
					 	   )
					betamount = self.betamount
				else:
					input("Press enter to exit >> ")

					exit()
			elif balance > stop:
				uiprint("Auto Stop goal reached. Betting has stopped.", "good")
				threading.Thread(target=playsounds, args=('Assets\Win.mp3',)).start()
				ToastNotifier().show_toast("Bloxflip Smart Bet", 
					   "Your auto stop goal has been reached!", duration = 3,
				 	   icon_path ="assets\\Bloxflip.ico",
				 	   threaded=True
				 	   )
				uiprint("If the program is reaching the goal instantly that likely means your balance is already above the auto_stop amount.", "warning")
				uiprint("To fix this simply increase the number to a number higher than your current balance.", "warning")
				input("Press enter to resume betting >> ")
				while True:
					try:
						stop = float(input("Enter new goal: "))
						break
					except:
						uiprint("Ivalid number.", "error")
			elif balance < stoploss:
				uiprint(f"Balance is below stop loss. All betting has stopped.", "bad")
				threading.Thread(target=playsounds, args=('Assets\Loss.mp3',)).start()
				ToastNotifier().show_toast("Bloxflip Smart Bet", 
					   "You've hit your stop loss!", duration = 3,
				 	   icon_path ="assets\\Bloxflip.ico",
				 	   threaded=True
				 	   )
				input("Press enter to exit >> ")
				exit()

			elif balance-betamount < stoploss:
				uiprint(f"Resetting bet amount to {self.betamount}; If game is lost balance will be under stop loss", "yellow")
				threading.Thread(target=playsounds, args=('Assets\Loss.mp3',)).start()
				ToastNotifier().show_toast("Bloxflip Smart Bet", 
					   "You've almost hit your stop loss! Resetting bet amount", duration = 3,
				 	   icon_path ="assets\\Bloxflip.ico",
				 	   threaded=True
				 	   )
				betamount = self.betamount

			if betamount > maxbet:
				uiprint(f"Resetting bet amount to {self.betamount}; Bet amount is above max_betamount:{maxbet}", "yellow")
				threading.Thread(target=playsounds, args=('Assets\Loss.mp3',)).start()
				ToastNotifier().show_toast("Bloxflip Smart Bet", 
					   "You've hit your maxbet! Resetting bet amount", duration = 3,
				 	   icon_path ="assets\\Bloxflip.ico",
				 	   threaded=True
				 	   )
				betamount = self.betamount
				continue
			
			if round(prediction, 2) <= 1:
				uiprint("Cancelling bet this game. As the game will likely crash around 1x.")
				continue

			if bet:
				uiprint(f"Placing bet with {betamount} Robux on {prediction}x multiplier")
				if self.webhook:
					sendwebhookmsg(self.webhook, f"Betting {betamount} Robux at {round(prediction,2)}x\n{round(balance-betamount,2)} Robux Left", f"Betting {betamount} Robux ", 0x903cde, f"")
					sendwebhookmsg(self.webhook,f"Average Crash : {round(avg,2)}\nMultiplier Set to : {multiplier}\n Accuracy on last crash : {accuracy}%","Round Predictions", 0xaf5ebd, f"")


				time.sleep(3)

				try:
					json = str({"autoCashoutPoint":int(prediction*100),"betAmount":betamount}).replace("'", '"').replace(" ", "")
					ws.send(f'42/crash,["join-game",{str(json)}]')
				except Exception as e:
					uiprint("Failed to join crash game! Reconnecting to server...")
					time.sleep(0.5)
					ws = self.Connect()
					ws.send("40/crash,")
					ws.send(f'42/crash,["auth","{self.auth}"]')

if __name__ == "__main__":
	main()