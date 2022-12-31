#!/usr/bin/env python -W ignore::DeprecationWarning 

import cloudscraper, subprocess, selenium, threading, websocket, requests, random, logging, base64, json, time, uuid, ssl, re, os
from bloxflip import Authorization, Authorization, Currency
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from websocket import create_connection
from win10toast import ToastNotifier
from playsound import playsound
from selenium import webdriver
from termcolor import cprint
from bloxflip import *
from zipfile import *
from sys import exit


class Main(Crash):
	def __init__(self) -> None:
		logging.basicConfig(filename="errors.txt", level=logging.DEBUG)
		subprocess.call('start "" "assets\config.mrc"', shell=True)
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

	def print(self, message: str = "", option="default") -> None: # print the ui's text with
		print("[ ", end="")

		key = {
			"default": ["AUTOBET", "magenta"],
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

	def clear(self) -> None: # Clear the console
		os.system('cls' if os.name == 'nt' else 'clear')

	def install_driver(self, version: str = None) -> None:
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

		options = webdriver.ChromeOptions()
		options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
		options.add_argument('--disable-extensions')
		options.add_argument('--profile-directory=Default')
		options.add_argument("--incognito")
		options.add_argument("--disable-plugins-discovery")
		options.add_experimental_option("excludeSwitches", ["enable-automation", 'enable-logging'])
		options.add_experimental_option('useAutomationExtension', False)		
		try:
			self.browser = webdriver.Chrome("chromedriver.exe", options=options)
		except selenium.common.exceptions.SessionNotCreatedException as e:
			try:
				print(e)
				self.installDriver(103)
				self.browser = webdriver.Chrome("chromedriver.exe", options=options)
			except:
				uiprint("Chromedriver version not compatible with current chrome version installed. Update your chrome to continue.", "error")
				uiprint("If your not sure how to update just uninstall then reinstall chrome", "yellow")
				time.sleep(5)
				os._exit(0)


	def setup(self) -> None: # Get configuration from config.json file
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
			self.multiplier = float(config["multiplier"])
			self.average = int(config["games_averaged"])
			self.auth = config["authorization"]
			self.key = config["key"]
			self.disablePredictor = not config["predict_crash"]
			self.martingale = config["martingale"]
			self.sound = config["play_sounds"]
			self.webhook = config["webhook"]
			self.betamount = float(config["bet_amount"])
			self.maxbet =  float(config["max_betamount"])
			self.skip =  config["skip_losing_streaks"]
			self.bet = float(config["auto_bet"])
			self.stop =  float(config["auto_stop"])
			self.stoploss =  float(config["stop_loss"])
			self.restart = config["auto_restart"]

			if self.multiplier < 2:
				uiprint("Multiplier must be above 2 to make profit.", "error")
				time.sleep(2)
				os._exit(0)

			if self.average > 35:
				uiprint("Too many games_averaged. Must be 35 or less games", "error")
				time.sleep(2)
				os._exit(0)

			if not "https://" in self.webhook:
				uiprint("Invalid webhook inside JSON file file. Make sure you put the https:// with it.", "warning")
				self.webhook = None

		except KeyError as e:
			uiprint(f"{k} Key is missing from JSON redownload from github", "error")
			time.sleep(2)
			os._exit(0)

		except ValueError as e:
			key = e.split("'")[1]
			uiprint(f"Invalid {key} inside json")
			time.sleep(2)
			os._exit(0)

		if not Authorization.validate(self.auth):
			uiprint("Invalid Authorization!", "error")
			time.sleep(2)
			os._exit(0)

		self.user = Authorization.get_info(self.auth)
		self.headers = {
			"x-auth-token": self.auth
		}

		if not type(self.restart) == bool:
			uiprint("Invalid auto_restart boolean inside JSON file. Must be true or false", "error")
			time.sleep(2)
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


		self.selenium_based = False

		super().__init__(self.auth)
		self.crash = super()

		max_retry = 5
		crash = self.crash
		while True:
			max_retry -= 1
			try:
				websocket = crash.Websocket()
				websocket.connect()

				self.websocket = websocket
				break
			except Exception as e:
				uiprint(f"Failed to connect to webserver. Retrying in 1.5 seconds, {max_retry} tries left.", "error")

				if max_retry <= 0:
						uiprint("Too many attempts, switching to selenium")
						self.selenium_based = True
						break
				time.sleep(1.5)

		if self.selenium_based:
			self.install_driver()
			browser = self.browser
			browser.get("https://bloxflip.com/a/BFSB") # Open browser
			while True:
				try:
					browser.execute_script(f'''localStorage.setItem("_DO_NOT_SHARE_BLOXFLIP_TOKEN", "{self.auth}")''') # Login with authorization
					browser.execute_script(f'''window.location = "https://bloxflip.com/a/BFSB"''')
					browser.execute_script(f'''window.location = "https://bloxflip.com/crash"''')
					break
				except Exception as e:
					Exception(e)
			time.sleep(3.2)

			self.updateBetAmount(self.betamount)
			self.updateMultiplier(self.multiplier)

	def playsounds(self, file: str) -> None:
		if self.sound:
			playsound(file)


	def start(self) -> None:
		uiprint = self.print
		uiprint("Betting started. Press Ctrl + C to exit")

		disablePredictor = self.disablePredictor
		selenium_based = self.selenium_based
		sendwebhookmsg = self.sendwbmsg
		multiplier = self.multiplier
		playsounds = self.playsounds
		martingale = self.martingale
		betamount = self.betamount
		stoploss = self.stoploss
		average = self.average
		restart = self.restart
		headers = self.headers
		webhook = self.webhook
		maxbet = self.maxbet
		crash = self.crash
		stop = self.stop
		skip = self.skip
		auth = self.auth
		lastgame = None
		bet = self.bet
		key = self.key
		winning = 0
		losing = 0

		prediction = multiplier
		failed = False
		pause = True

		if selenium_based:
			browser = self.browser
		else:
			websocket = self.websocket

		for games in crash.crashpoints():
			uiprint("Game Starting...")
			balance = Currency.balance(auth)

			games = [game.crashpoint for game in games]
			avg = sum(games[-3:])/len(games[-3:])
			lastgame = games[0]
			accuracy = None
			
			streak = [1, 0]
			uiprint(f"Average Crashpoint: {avg}")


			for game in games:
				if game > 2:
					streak[0] += 1
				else:
					streak[1] += 1

			try:
				if not failed:
					if lastgame >= prediction:
						if not self.webhook == None:
							sendwebhookmsg(self.webhook, f"You have made {betamount*multiplier - betamount} robux", f"You Won!", 0x83d687, f"")

						if martingale and not pause:
							betamount = self.betamount
							uiprint(f"Won previous game. lowering bet amount to {betamount}", "good")
							
						pause = False
						
							
						try:
							threading.Thread(target=playsounds, args=('Assets\Win.mp3',)).start()
						except:
							pass
					else:
						if martingale and not pause:
							betamount *= 2
							uiprint(f"Lost previous game. Increasing bet amount to {betamount}", "bad")

							
						pause = False
						if not self.webhook == None:
							sendwebhookmsg(self.webhook, f"You lost {betamount} robux\n You have {balance} left", f"You Lost!", 0xcc1c16, f"")
						
						try:
							threading.Thread(target=playsounds, args=('Assets\Loss.mp3',)).start()
						except:
							pass

					if selenium_based:
						self.updateBetAmount(betamount)

				else:
					uiprint(f"Failed to place bet last game retrying with {betamount}", "warning")
					failed = False
				
			except (ValueError, TypeError, UnboundLocalError, NameError):
				uiprint(f"No data for accuracy calculations", "error")


			if streak[0] >= streak[1]:
				uiprint("Winning streak detected.", "good")
			else:
				uiprint("Losing streak detected", "bad")
				if skip:
					uiprint("Skipping this round.", "warning")
					pause = True
					continue

			try:
				games[0]
			except:
				continue
			
			
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
				continue

			if bet:
				uiprint(f"Placing bet with {betamount} Robux on {prediction}x multiplier")
				if self.webhook:
					sendwebhookmsg(self.webhook, f"Betting {betamount} Robux at {round(prediction,2)}x\n{round(balance-betamount,2)} Robux Left", f"Betting {betamount} Robux ", 0x903cde, f"")
					sendwebhookmsg(self.webhook,f"Average Crash : {round(avg,2)}\nMultiplier Set to : {multiplier}\n Accuracy on last crash : {accuracy}%","Round Predictions", 0xaf5ebd, f"")


				time.sleep(3)

				if not selenium_based:
					try:
						websocket.join(betamount=betamount, multiplier=prediction)
					except Exception as e:
						uiprint("Failed to join crash game! Reconnecting to server...", "error")
						websocket = crash.Websocket()
						websocket.connect()
						failed = True
				else:
					try:
						browser.find_element(By.CSS_SELECTOR, ".button_button__eJwei.button_primary__mdLFG.gameBetSubmit").click()
					except Exception as e:
						failed = True
						uiprint("Failed to join crash game!", "error")
						print(e)


if __name__ == "__main__":
	Main()
