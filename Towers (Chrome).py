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
		self.version = "1.2.7"
		os.system("")
		try:
			self.getConfig()
			self.sendBets()
		except KeyboardInterrupt:
			self.print("Exiting program.")
			self.browser.close()
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
		element = self.browser.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/header/div/div[1]/div/div/span/span')[0]
		val = float(element.text.replace(",", ''))
		return val

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
				self.levels = int(config["tower_levels"])
				if self.levels < 2:
					uiprint("Levels must be above 2 to make profit.", "error")
					time.sleep(3)
					exit()
			except ValueError as e:
				uiprint("Invalid levels inside JSON file. Must be valid number", "error")
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


			self.installDriver()
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

			browser = self.browser
			browser.get("https://bloxflip.com/a/SmartBet") # Open browser
			while True:
				try:
					browser.execute_script(f'''localStorage.setItem("_DO_NOT_SHARE_BLOXFLIP_TOKEN", "{self.auth}")''') # Login with authorization
					browser.execute_script(f'''window.location = "https://bloxflip.com/a/SmartBet"''')
					browser.execute_script(f'''window.location = "https://bloxflip.com/towers"''')
					break
				except Exception as e:
					Exception(e)
			time.sleep(3.8)

			notLoggedIn = self.browser.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/header/div/div/button')[0].text
			if notLoggedIn:
				self.print("Please put a valid authorization token in the config.json file. Exiting program.", "error")
				browser.quit()
				exit()

			elements = browser.find_elements(By.CSS_SELECTOR, '.input_input__uGeT_.input_inputWithCurrency__sAiOQ')
			if not elements:
				uiprint("Blocked by DDoS protection. Solve the captcha on the chrome window to continue.")
			while not elements:
				elements = browser.find_elements(By.CSS_SELECTOR, '.input_input__uGeT_.input_inputWithCurrency__sAiOQ')

			try:
				for _ in range(10):
					elements[0].send_keys(f"{Keys.BACKSPACE}")
				elements[0].send_keys(f"{self.betamount}",Keys.BACKSPACE)
			except:
				uiprint("Tower game aready in progress. End the game then try again", "error")
				time.sleep(3)
				exit()



	def playsounds(self, file):
		if self.sound:
			playsound(file)


	def updateBetAmount(self, amount):
		browser = self.browser
		elements = browser.find_elements(By.CSS_SELECTOR, '.input_input__uGeT_.input_inputWithCurrency__sAiOQ')
		for _ in range(10):
			elements[0].send_keys(f"{Keys.BACKSPACE}")
		elements[0].send_keys(f"{amount}",Keys.BACKSPACE)

	def playsounds(self, file):
		if self.sound:
			playsound(file)

	def TowerGames(self):
		browser = self.browser
		average = self.average
		history = None
		uiprint = self.print
		sent = False
		
		scraper = cloudscraper.create_scraper()
		

		while True:
			games = scraper.get('https://rest-bf.blox.land/games/towers', headers={"x-auth-token":self.auth}).json()
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
		browser = self.browser
		average = self.average
		restart = self.restart
		webhook = self.webhook
		levels = self.levels
		maxbet = self.maxbet
		stop = self.stop
		lastgame = None
		bet = self.bet
		key = self.key
		winning = 0
		losing = 0


		oldbalance = getBalance()
		balance = getBalance()


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
						self.updateBetAmount(betamount)
					except:
						uiprint("Tower game aready in progress. End the game then try again", "error")
						time.sleep(3)
						exit()

						
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
						self.updateBetAmount(betamount)
					except Exception as e:
						uiprint("Tower game aready in progress. End the game then try again", "error")
						time.sleep(3)
						exit()
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
					browser.close()
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
				browser.close()
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
				self.updateBetAmount()

			if betamount > maxbet:
				uiprint(f"Resetting bet amount to {self.betamount}; Bet amount is above max_betamount:{maxbet}", "yellow")
				threading.Thread(target=playsounds, args=('Assets\Loss.mp3',)).start()
				ToastNotifier().show_toast("Bloxflip Smart Bet", 
					   "You've hit your maxbet! Resetting bet amount", duration = 3,
				 	   icon_path ="assets\\Bloxflip.ico",
				 	   threaded=True
				 	   )
				betamount = self.betamount
				self.updateBetAmount()
 

			balance = getBalance()
			browser.execute_script("arguments[0].click();", browser.find_element(By.CSS_SELECTOR, ".button_button__eJwei.button_primary__mdLFG.gameBetSubmit"))
			uiprint(f"Placing bet with {betamount} Robux")
			

			rows = browser.find_element(By.CSS_SELECTOR, ".towers_towersGameInner__teKsK").find_elements(By.XPATH, "./*")
			time.sleep(2.5)
			for i in range(levels):
				while True:
					request = requests.get("https://bfpredictor.repl.co/towers", 
											data={
												"key": key
											}
										)

					if request.status_code == 403:
						uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/HhwNFRaC", "error")
						input("Press enter to exit >> ")
						browser.close()
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

				element = rows[-(i+1)].find_elements(By.XPATH, "./*")[choice]

				element = element.find_elements(By.XPATH, "./*")[0]
				while True:
					try:
						browser.execute_script("arguments[0].click();", element)
					except Exception as e:
						print(e)
					break
				time.sleep(1.5)
			


			if webhook:
				sendwebhookmsg(self.webhook, f"Betting {betamount} Robux\n{round(balance-betamount,2)} Robux Left", f"Betting {betamount} Robux ", 0x903cde, f"")
			try:
				browser.find_element(By.XPATH, "//span[contains(text(),'Cashout')]").click()
			except:
				try:
					browser.execute_script("arguments[0].click();", browser.find_element(By.CSS_SELECTOR, ".button_button__eJwei.button_secondary__dwIbt.gameBetSubmit"))
				except:
					try:
						browser.find_element(By.CSS_SELECTOR, ".button_button__eJwei.button_secondary__dwIbt.gameBetSubmit").click()
					except:
						pass

			time.sleep(1.5)

if __name__ == "__main__":
	main()