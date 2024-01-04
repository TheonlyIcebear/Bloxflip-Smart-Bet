#!/usr/bin/env python -W ignore::DeprecationWarning 

import cloudscraper, subprocess, selenium, threading, websocket, requests, random, logging, base64, json, time, ssl, os
from bloxflip import Authorization, Jackpot, Currency
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from websocket import create_connection
from win10toast import ToastNotifier
from playsound import playsound
from selenium import webdriver
from random import randbytes
from termcolor import cprint
from zipfile import *
from sys import exit


class Main(Jackpot):
	def __init__(self):
		logging.basicConfig(filename="errors.txt", level=logging.DEBUG)
		self.crashPoints = None
		self.multiplier = 0
		self.version = "1.3.3"
		os.system("")
		try:
			self.setup()
			self.start()
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

	def print(self, message: str = "", option: str = "default") -> None: # print the ui's text with
		print("[ ", end="")

		key = {
			"default": ["AUTOBET", "magenta"],
			"error": ["ERROR", "red"],
			"warning": ["WARNING", "yellow"],
			"yellow": ["AUTOBET", "yellow"],
			"good": ["AUTOBET", "green"],
			"bad": ["AUTBET", "red"]
		}

		title = key[option][0]
		color = key[option][1]

		cprint(title, color, end="")
		print(" ] ", end="")
		cprint(message, color)

	def sendwbmsg(self, url: str, message: str, title: str, color: str, content: str) -> None:
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


	def Connect(self):
		return create_connection("wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket",
								suppress_origin=True, 
								header={
										"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
										"Accept": "*/*",
										"Accept-Language": "en-US,en;q=0.5",
										"Accept-Encoding": "gzip, deflate, br",
										"Sec-WebSocket-Version": "13",
										"Origin": "https://www.piesocket.com",
										"Sec-WebSocket-Extensions": "permessage-deflate",
										"Sec-WebSocket-Key": str(base64.b64encode(randbytes(16)).decode('utf-8')),
										"Connection": "keep-alive, Upgrade",
										"Sec-Fetch-Dest": "websocket",
										"Sec-Fetch-Mode": "websocket",
										"Sec-Fetch-Site": "cross-site",
										"Pragma": "no-cache",
										"Cache-Control": "no-cache",
										"Upgrade": "websocket"
				}
			)


	def setup(self): # Get configuration from config.json file
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
			uiprint("config.json file is missing or invalid JSON format. Please redownload the config.json from the Github", "error")

		with open("config.json", "r+") as data:
			try:
				config = json.load(data)
				self.chance = float(config["chanceof_winning"])
				self.snipe = float(config["snipe_at"])
				self.auth = config["authorization"]
				self.key = config["key"]
				self.disablePredictor = not config["predict_crash"]
				self.sound = config["play_sounds"]
				self.webhook = config["webhook"]
				self.maxbet =  float(config["max_betamount"])
				self.bet = float(config["auto_bet"])
				self.stop =  float(config["auto_stop"])
				self.stoploss =  float(config["stop_loss"])
				self.restart = config["auto_restart"]
			except KeyError as k:
				uiprint(f"{k} is missing from JSON file. Redownload from the github", "error")
				time.sleep(1.6)
				os._exit(0)
			except Exception as e:
				uiprint("An error has occured", "error")
				print(e)
				time.sleep(1.6)
				os._exit(0)

			if not "https://" in self.webhook:
				uiprint("Invalid webhook inside JSON file file. Make sure you put the https:// with it.", "warning")
				self.webhook = None


			if not type(self.restart) == bool:
				uiprint("Invalid auto_restart boolean inside JSON file. Must be true or false", "error")
				time.sleep(1.6)
				os._exit(0)
			self.hwid = current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

			version = self.version
			latest_release = requests.get("https://bfpredictor.repl.co/latest_release").text
			if latest_release == version:
				uiprint("Your version is up to date.", "good")
			else:
				uiprint(f"You are currently on v{version}. Please update to the newest version {latest_release}", "error")
				time.sleep(10)
				os._exit(0)

			self.headers = {
				"x-auth-token": self.auth
			}

			super().__init__(self.auth)
			self.jackpot = super()

			if not Authorization.validate(self.auth):
				uiprint("Invalid Authorization!", "error")
				time.sleep(2)
				os._exit(0)

			max_retry = 5
			jackpot = self.jackpot
			while True:
				max_retry -= 1
				try:
					websocket = jackpot.Websocket()
					websocket.connect()
					break
				except Exception as e:
					print(e)
					uiprint(f"Failed to connect to webserver. Retrying in 1.5 seconds, {max_retry} tries left.", "error")
					if max_retry <= 0:
							uiprint("Too many attempts, try again later.", "errors")
							time.sleep(1.5)
							os._exit(0)
					time.sleep(1.5)

			self.websocket = websocket

	def playsounds(self, file: str) -> None:
		if self.sound:
			playsound(file)


	def start(self) -> None: # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("Betting started. Press Ctrl + C to exit")

		disablePredictor = self.disablePredictor
		sendwebhookmsg = self.sendwbmsg
		playsounds = self.playsounds
		websocket = self.websocket
		stoploss = self.stoploss
		restart = self.restart
		webhook = self.webhook
		headers = self.headers
		jackpot = self.jackpot
		chance = self.chance
		maxbet = self.maxbet
		snipe = self.snipe
		stop = self.stop
		lastgame = None
		auth = self.auth
		bet = self.bet
		key = self.key
		winning = 0
		losing = 0
		pause = True

		scraper = cloudscraper.create_scraper()	

		for pot in jackpot.sniper(snipe_at=snipe):
			uiprint("Game Starting...")

			uiprint(f"Pot value: {pot.value}")
			balance = Currency.balance(auth)

			while True:
				request = scraper.get("https://bfpredictor.repl.co/jackpot", 
										data={"key": key,
											  "value": pot.value,
											  "hwid": self.hwid,
											  "chance": chance
										}
									)

				if request.status_code == 403:
					uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/blox", "error")
					input("Press enter to exit >> ")

					os._exit(0)
				elif request.status_code == 500:
					uiprint("Internal server error. Trying again 1.5 seconds...", "error")
					time.sleep(1.5)
				elif request.status_code == 200:
					betamount = round(float(request.text))
					break
				else:
					uiprint("Internal server error. Trying again 1.5 seconds...", "error")
					time.sleep(1.5)


			uiprint(f"Setting betamount to {betamount}", "yellow")

			
			uiprint(f"Your balance is {balance}")
			if balance < betamount:
				uiprint("Pot is too expensive to bet. Skipping this round", "error")
				continue
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

			if betamount > maxbet:
				uiprint("Pot is too expensive to bet. Skipping this round", "error")
				continue


			if bet:
				uiprint(f"Placing bet with {betamount} Robux with a {chance}% of winning")
				if self.webhook:
					sendwebhookmsg(self.webhook, f"Betting {betamount} Robux with a {chance}% chance of winning\n{round(balance-betamount,2)} Robux Left", f"Betting {betamount} Robux ", 0x903cde, f"")

				try:
					websocket.join()
				except Exception as e:
					uiprint("Failed to join jackpot game! Reconnecting to server...", "error")
					websocket = jackpot.Websocket()
					websocket.connect()

if __name__ == "__main__":
	Main()
