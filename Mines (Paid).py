#!/usr/bin/env python -W ignore::DeprecationWarning 

import cloudscraper, subprocess, threading, selenium, requests, logging, base64, json, time, os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from playsound import playsound
from selenium import webdriver
from termcolor import cprint
from zipfile import *
from sys import exit



class main:
	def __init__(self):
		logging.basicConfig(filename="errors.txt", level=logging.DEBUG)
		self.crashPoints = None
		self.multiplier = 0
		self.version = "1.2.8"
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


	def installDriver(self, version=None):
		uiprint = self.print
		if not version:
			uiprint("Installing newest chrome driver...", "warning")
			latest_version = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
		else:
			uiprint(f"Installing version {version} chrome driver...", "warning")
			latest_version = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}").text
		download = requests.get(f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_win32.zip")


		
		subprocess.call('taskkill /im "chromedriver.exe" /f')
		try:
			os.chmod('chromedriver.exe', 0o777)
			os.remove("chromedriver.exe")
		except:
			pass


		with open("chromedriver.zip", "wb") as zip:
			zip.write(download.content)


		with ZipFile("chromedriver.zip", "r") as zip:
			zip.extract("chromedriver.exe")
		os.remove("chromedriver.zip")
		uiprint("Chrome driver installed.", "good")

	def getBalance(self):
		uiprint = self.print
		balance = None
		# browser = self.browser

		scraper = cloudscraper.create_scraper()
		try: 
			balance = scraper.get("https://rest-bf.blox.land/user", headers={
						"x-auth-token": self.auth
				}).json()["user"]["wallet"]
		except Exception as e:
			print(e)
			uiprint("Invalid authorization. Make sure you copied it correctly, and for more info check the github", "bad")
			time.sleep(1.7)
			exit()
		return round(balance, 2)

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
			config = json.load(data)
			try:
				self.levels = int(config["game_levels"])
				if self.levels < 2:
					uiprint("Levels must be above 2 to make profit.", "error")
					time.sleep(3)
					exit()
			except:
				uiprint("Invalid levels inside JSON file. Must be valid number", "error")
				time.sleep(1.6)
				exit()


			try:
				self.mines = float(config["mines"])
			except Exception as e:
				print(e)
				uiprint(f"Invalid bet_amount inside JSON file. Must be valid number", "error")
				time.sleep(1.6)
				exit()

			try:
				self.average = int(config["games_averaged"])
				if self.average > 35:
					uiprint("Too many games_averaged. Must be 35 or less games", "error")
					time.sleep(3)
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
				uiprint("Invalid webhook boolean inside JSON file. Make sure it's a valid string", "error")
				time.sleep(1.6)
				exit()

			try:
				self.betamount = float(config["bet_amount"])
				if not self.betamount >= 5:
					uiprint("Invalid bet_amount inside JSON file. Must be above 5")
					time.sleep(3)
					exit()
			except Exception as e:
				print(e)
				uiprint(f"Invalid bet_amount inside JSON file. Must be valid number", "error")
				time.sleep(1.6)
				exit()


			try:
				self.maxbet =  float(config["max_betamount"])
			except:
				uiprint("Invalid max_betamount amount inside JSON file. Must be a valid number", "error")
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

			version = self.version
			data = {"type": "paid"}
			latest_release = requests.get("https://bfpredictor.repl.co/latest_release").text
			if latest_release == version:
				uiprint("Your version is up to date.", "good")
			else:
				uiprint(f"You are currently on v{version}. Please update to the newest version {latest_release}", "error")
				time.sleep(10)
				exit()

			request = requests.get("https://bfpredictor.repl.co/mines", 
										data={
											"key": self.key
										}
									)

			if request.status_code == 403:
				uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/HhwNFRaC", "error")
				input("Press enter to exit >> ")
				exit()


	def playsounds(self, file):
		if self.sound:
			playsound(file)

	def TowerGames(self):
		average = self.average
		history = None
		uiprint = self.print
		sent = False
		
		scraper = cloudscraper.create_scraper()
		

		while True:
			games = scraper.get('https://rest-bf.blox.land/games/mines', headers={"x-auth-token":self.auth}).json()
			time.sleep(10)
			if not games["hasGame"]:
				try:
					data = scraper.get('https://rest-bf.blox.land/user/wallet-history?size=10&page=0', headers={"x-auth-token":self.auth}).json()
					amount = data["data"][0]["amount"]
					uuid = data["data"][0]["extraData"]["uuid"]
					if not sent: 
						sent = True
						raise
				except Exception as e:
					amount = 0
					uuid = 0
				yield [amount, uuid]
			time.sleep(0.1)

	def sendBets(self): # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("Betting started. Press Ctrl + C to exit")

		sendwebhookmsg = self.sendwbmsg
		playsounds = self.playsounds
		getBalance = self.getBalance
		betamount = self.betamount
		stoploss = self.stoploss
		average = self.average
		restart = self.restart
		webhook = self.webhook
		levels = self.levels
		maxbet = self.maxbet
		mines = self.mines
		stop = self.stop
		auth = self.auth
		lastgame = None
		bet = self.bet
		key = self.key
		winning = 0
		losing = 0


		scraper = cloudscraper.create_scraper()
		oldbalance = getBalance()
		balance = getBalance()

		headers = {
					"x-auth-token": auth,
				}
		


		while True:
			uiprint("Game Starting...")
			balance = self.getBalance()

			accuracy = None
			
			amount = -1 * (oldbalance-balance)
			oldbalance = balance


			try:
				if amount > 0:
					if not self.webhook == None:
						sendwebhookmsg(self.webhook, f"You have made {amount} robux", f"You Won!", 0x83d687, f"")
					uiprint(f"Won R${amount} during previous game. lowering bet amount to {self.betamount}", "good")

					betamount = self.betamount

						
					try:
						threading.Thread(target=playsounds, args=('Assets\Win.mp3',)).start()
					except:
						pass
				elif amount < 0:
					uiprint(f"Lost R${abs(amount)} during previous game. Increasing bet amount to {betamount*2}", "bad")
					betamount *= 2
					if not self.webhook == None:
						sendwebhookmsg(self.webhook, f"You lost {betamount} robux\n You have {balance} left", f"You Lost!", 0xcc1c16, f"")

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
 

			balance = getBalance()
			response = scraper.post("https://rest-bf.blox.land/games/mines/create", 
								headers=headers, 
								json={
									"betAmount": betamount,
									"mines": mines
								}
						)


			if not response.status_code == 200:
				uiprint("Failed to place bet.", "error")
				try:
					response.json()
				except:
					uiprint("Network error.", "error")
					continue
				if response.json()["msg"] == "You already have an active mines game!":
					uiprint("You already have a active mines game! end it then try again")
					time.sleep(5)
					exit()
				continue
			uiprint(f"Placing bet with {betamount} Robux")
			

			time.sleep(2.5)
			exploded = False
			for level in range(levels):
				while True:
					request = requests.get("https://bfpredictor.repl.co/mines", 
											data={
												"key": key
											}
										)

					if request.status_code == 403:
						uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/HhwNFRaC", "error")
						input("Press enter to exit >> ")
						exit()
					elif request.status_code == 500:
						uiprint("Internal server error. Trying again 1.5 seconds...", "error")
						time.sleep(1.5)
					elif request.status_code == 200:
						choice = int(request.text)
						break
					else:
						uiprint("Internal server error. Trying again 1.5 seconds...", "error")
						time.sleep(1.5)
				uiprint(f"Choosing button number {choice+1}")
				response = scraper.post("https://rest-bf.blox.land/games/mines/action", 
								headers=headers,
								json={
									"cashout": False,
									"mine": choice
								}
						)
				

				if not response.status_code == 200:
					if response.json()["msg"] == "You do not have an active mines game!":
						exploded = True
						continue
				
				time.sleep(0.3)

				try:
					response.json()["exploded"]
				except:
					exploded = True
					continue

				if response.json()["exploded"] == True:
					exploded = True
					continue

				uiprint(f"Successfully passed level {level+1}", "good")

			if exploded:
					uiprint("Mine exploded!", "bad")
					continue					
			


			if webhook:
				sendwebhookmsg(self.webhook, f"Betting {betamount} Robux\n{round(balance-betamount,2)} Robux Left", f"Betting {betamount} Robux ", 0x903cde, f"")
			response = scraper.post("https://rest-bf.blox.land/games/mines/action", 
								headers=headers,
								json={
									"cashout": True,

								}
						)
			while not response.status_code == 200:
					uiprint("Failed to cashout trying again in 1.5 seconds...")
					time.sleep(1.5)

					response = scraper.post("https://rest-bf.blox.land/games/mines/action", 
								headers=headers,
								json={
									"cashout": True,

								}
						)

			time.sleep(1.5)

if __name__ == "__main__":
	main()