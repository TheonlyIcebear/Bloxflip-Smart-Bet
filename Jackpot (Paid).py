#!/usr/bin/env python -W ignore::DeprecationWarning 

import cloudscraper, subprocess, selenium, threading, websocket, requests, random, logging, base64, json, time, ssl, os
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



class main:
	def __init__(self):
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		logging.basicConfig(filename="errors.txt", level=logging.DEBUG)
		self.crashPoints = None
		self.multiplier = 0
		self.version = "1.31"
		os.system("")
		try:
			threading.Thread(target=self.proxySwap).start()
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


	def proxySwap(self):
		while True:
			self.proxies = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=1000&country=US&ssl=all&anonymity=all").text.splitlines()
			time.sleep(60)


	def proxy(self):
		return "socks5://"+random.choice(self.proxies)


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


	def updateBetAmount(self, amount):
		browser = self.browser
		uiprint = self.print
		try:
			element = browser.find_elements(By.CSS_SELECTOR, 'input.input_input__uGeT_.input_inputWithCurrency__sAiOQ')[0]
		except IndexError:
			uiprint("Blocked by ddos protection sove the captcha to continue")
			while True:
				try:
					element = browser.find_elements(By.CSS_SELECTOR, 'input.input_input__uGeT_.input_inputWithCurrency__sAiOQ')[0]
					break
				except IndexError:
					pass

		for _ in range(10):
			element.send_keys(f"{Keys.BACKSPACE}")
		element.send_keys(f"{amount}")

	def updateMultiplier(self, multiplier):
		browser = self.browser
		uiprint = self.print
		try:
			element = browser.find_elements(By.CSS_SELECTOR, '.input_input__uGeT_')[1]
		except IndexError:
			uiprint("Blocked by ddos protection sove the captcha to continue")
			while True:
				try:
					element = browser.find_elements(By.CSS_SELECTOR, '.input_input__uGeT_')[1]
					break
				except IndexError:
					pass
		time.sleep(0.2)
		for _ in range(10):
			element.send_keys(f"{Keys.BACKSPACE}")
		element.send_keys(f"{multiplier}")


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
										"Upgrade": "websocket",
										"x-auth-token": self.auth
				}
			)

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
				exit()


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
				exit()
			except Exception as e:
				uiprint("An error has occured", "error")
				print(e)
				time.sleep(1.6)
				exit()

			if not "https://" in self.webhook:
				uiprint("Invalid webhook inside JSON file file. Make sure you put the https:// with it.", "warning")
				self.webhook = None


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

			self.headers = {
							"x-auth-token": self.auth
						}

			max_retry = 5
			while True:
				max_retry -= 1
				try:
					self.ws = self.Connect()
					break
				except Exception as e:
					uiprint(f"Failed to connect to webserver. Retrying in 1.5 seconds, {max_retry} tries left.", "error")
					if max_retry <= 0:
							uiprint("Too many attempts, try again later.", "errors")
							time.sleep(1.5)
							exit()
					time.sleep(1.5)

			ws = self.ws
			ws.send("40/jackpot,")
			ws.send(f'42/jackpot,["auth","{self.auth}"]')


	def proxySwap(self):
		while True:
			self.proxies = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=1000&country=US&ssl=all&anonymity=all").text.splitlines()
			time.sleep(60)


	def proxy(self):
		return "socks5://"+random.choice(self.proxies)


	def Jackpots(self):
		history = None
		reset = False
		uiprint = self.print
		snipe = self.snipe
		sent = False

		scraper = cloudscraper.create_scraper()

		while True:
			if not reset:
				try:
					current = scraper.get("https://api.bloxflip.com/games/jackpot", headers={
							"x-auth-token": self.auth
						})
					elapsed = current.elapsed.total_seconds()
					current = current.json()["current"]
				except Exception as e:
					print(e)

				if len(current["players"]) == 2:
					time.sleep(1)
					reset = True
					start = time.time()
					timeleft = round((32-(time.time()-start))+elapsed, 2)

			else:
				timeleft = round((32-(time.time()-start))+elapsed, 2)


			try:
				timeleft
			except:
				continue


			if not history == current["_id"]:
				if timeleft <= snipe:
					current = scraper.get("https://api.bloxflip.com/games/jackpot", headers={
							"x-auth-token": self.auth
						}).json()["current"]
					history = current["_id"]
					reset = False
					yield sum([player["betAmount"] for player in current["players"]])
			time.sleep(0.01)

	def playsounds(self, file):
		if self.sound:
			playsound(file)


	def sendBets(self): # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("Betting started. Press Ctrl + C to exit")

		disablePredictor = self.disablePredictor
		sendwebhookmsg = self.sendwbmsg
		playsounds = self.playsounds
		stoploss = self.stoploss
		restart = self.restart
		webhook = self.webhook
		headers = self.headers
		chance = self.chance
		maxbet = self.maxbet
		stop = self.stop
		lastgame = None
		bet = self.bet
		key = self.key
		ws = self.ws
		winning = 0
		losing = 0
		pause = True

		scraper = cloudscraper.create_scraper()	

		for pot in self.Jackpots():
			uiprint("Game Starting...")
			uiprint(f"Pot value: {pot}")
			balance = self.getBalance()

			while True:
				request = scraper.get("https://bfpredictor.repl.co/jackpot", 
										data={"key": key,
											  "value": pot,
											  "hwid": self.hwid,
											  "chance": chance
										}, headers=headers
									)

				print(request.text)
				if request.status_code == 403:
					uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/blox", "error")
					input("Press enter to exit >> ")

					exit()
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

			if betamount > maxbet:
				uiprint("Pot is too expensive to bet. Skipping this round", "error")
				continue


			if bet:
				uiprint(f"Placing bet with {betamount} Robux with a {chance}% of winning")
				if self.webhook:
					sendwebhookmsg(self.webhook, f"Betting {betamount} Robux with a {chance}% chance of winning\n{round(balance-betamount,2)} Robux Left", f"Betting {betamount} Robux ", 0x903cde, f"")

				try:
					json = str({"betAmount":betamount}).replace("'", '"').replace(" ", "")
					ws.send(f'42/jackpot,["join-game",{str(json)}]')
				except Exception as e:
					uiprint("Failed to join jackpot game! Reconnecting to server...", "error")
					ws = self.Connect()
					ws.send("40/jackpot,")
					ws.send(f'42/jackpot,["auth","{self.auth}"]')
if __name__ == "__main__":
	main()
