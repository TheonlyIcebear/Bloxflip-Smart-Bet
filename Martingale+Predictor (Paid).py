#!/usr/bin/env python -W ignore::DeprecationWarning 

# DISCLAIMER :: imo bloxflip seems to have updated their way of generating the crashpoint so prediction will be less accurate and useful
# --- the crash seems to be lower more often, but it also goes high (high as in about 5-20) more often than normal
# --- high crashpoints also seem to come in batches less often

# PATCH BY Oi#6369 | Discord

# General --
# 1 Option to disable updating to newest chrome drivers;
# 2 Correctly logs in on new site;
# 3 If you leave the crash page of bloxflip, the script won't crash anymore but redirect you back to crash;
# 4 Option to disable the predictor;

# New site --
# - UPDATED CSS SELECTORS;
# 1 Is able to correctly set bet amount upon starting;
# 2 Correctly updates bet- and multiplier amount;
# 3 Actually sends the bets on the new site;

# Patches --
# 1 Temporary fix for bloxflip API 403 (forbidden) error on getting balance using scraping. 
# -- there is one downside to this, all your balance gets rounded up above something.5 and down below that so there will be no floating point values.
# -- This makes playing at below 1 robux total balance basically impossible, keep this in mind

import subprocess, threading, selenium, requests, logging, base64, json, time, os
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
		notLoggedIn = self.browser.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/header/div/div/button')[0].text
		if notLoggedIn:
			self.print("Please put a valid authorization token in the config.json file. Exiting program.", "error")
			self.browser.close()
			exit()

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
			browser.get("https://bloxflip.com/crash") # Open browser
			while True:
				try:
					browser.execute_script(f'''localStorage.setItem("_DO_NOT_SHARE_BLOXFLIP_TOKEN", "{self.auth}")''') # Login with authorization
					browser.execute_script(f'''window.location = "https://bloxflip.com/a/BFSB"''')
					browser.execute_script(f'''window.location = "https://bloxflip.com/crash"''')
					break
				except Exception as e:
					Exception(e)
			time.sleep(3.2)

			notLoggedIn = self.browser.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/header/div/div/button')[0].text
			if notLoggedIn:
				self.print("Please put a valid authorization token in the config.json file. Exiting program.", "error")
				browser.quit()
				exit()

			elements = browser.find_elements(By.CSS_SELECTOR, '.input_input__uGeT_')
			if not elements:
				uiprint("Blocked by DDoS protection. Solve the captcha on the chrome window to continue.")
			while not elements:
				elements = browser.find_elements(By.CSS_SELECTOR, '.input_input__uGeT_')


			for _ in range(10):
				elements[0].send_keys(f"{Keys.BACKSPACE}")
			elements[0].send_keys(f"{self.betamount}")


			for _ in range(10):
				elements[1].send_keys(f"{Keys.BACKSPACE}")
			elements[1].send_keys(f"{self.multiplier}")

	def ChrashPoints(self):
		browser = self.browser
		average = self.average
		history = None
		uiprint = self.print
		sent = False

		while True:
			try:
				games = browser.execute_script("""return fetch('https://rest-bf.blox.land/games/crash').then(res => res.json());""")
			except:
				games = browser.execute_script("""return fetch('https://rest-bf.blox.land/games/crash').then(res => res.json());""")

			if not history == games["history"]:
				history = games["history"]
				yield [games["history"][0]["crashPoint"], [float(crashpoint["crashPoint"]) for crashpoint in history]]
			time.sleep(0.01)

	def playsounds(self, file):
		if self.sound:
			playsound(file)


	def updateBetAmount(self, amount):
		browser = self.browser
		element = browser.find_elements(By.CSS_SELECTOR, 'input.input_input__uGeT_.input_inputWithCurrency__sAiOQ')[0]
		for _ in range(10):
			element.send_keys(f"{Keys.BACKSPACE}")
		element.send_keys(f"{amount}")

	def updateMultiplier(self, multiplier):
		browser = self.browser
		element = browser.find_elements(By.CSS_SELECTOR, '.input_input__uGeT_')[1]
		time.sleep(0.2)
		for _ in range(10):
			element.send_keys(f"{Keys.BACKSPACE}")
		element.send_keys(f"{multiplier}")

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
		betamount = self.betamount
		stoploss = self.stoploss
		browser = self.browser
		average = self.average
		restart = self.restart
		webhook = self.webhook
		maxbet = self.maxbet
		stop = self.stop
		lastgame = None
		bet = self.bet
		key = self.key
		winning = 0
		losing = 0

		prediction = multiplier

		for game in self.ChrashPoints():
			uiprint("Game Starting...")
			balance = self.getBalance()

			games = game[1][-2:]
			rgames = game[1][-7:]
			accuracy = None
			lastgame = game[0]
			avg = sum(games)/len(games)
			streak = [0, 0]
			uiprint(f"Average Crashpoint: {avg}")


			try:
				if lastgame >= prediction:
					if not self.webhook == None:
						sendwebhookmsg(self.webhook, f"You have made {betamount*multiplier - betamount} robux", f"You Won!", 0x83d687, f"")
					betamount = self.betamount
					accuracy = (1-(lastgame-prediction)/lastgame)*100

					uiprint(f"Won previous game. lowering bet amount to {betamount}", "good")
					if not disablePredictor:
						uiprint(f"Accuracy on last guess: {accuracy}", "yellow")
					try:
						self.updateBetAmount(betamount)
					except Exception as e:
						uiprint(f"Input box for bet amount not found: {e}\n Redirecting to crash page", "error")
						browser.execute_script(f'window.location = "https://bloxflip.com/crash"')
						self.updateBetAmount(betamount)
						
					try:
						threading.Thread(target=playsounds, args=('Assets\Win.mp3',)).start()
					except:
						pass
				else:
					betamount *= 2
					uiprint(f"Lost previous game. Increasing bet amount to {betamount}", "bad")
					if not self.webhook == None:
						sendwebhookmsg(self.webhook, f"You lost {betamount} robux\n You have {balance} left", f"You Lost!", 0xcc1c16, f"")
					accuracy = (1-((prediction-lastgame)/lastgame))*100
					if not disablePredictor:
						uiprint(f"Accuracy on previous guess: {accuracy}", "yellow")
					try:
						self.updateBetAmount(betamount)
					except Exception as e:
						uiprint(f"Input box for bet amount not found: {e}\n Redirecting to crash page", "error")
						browser.execute_script(f'window.location = "https://bloxflip.com/crash"')
						self.updateBetAmount(betamount)
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

			try:
				games[0]
			except:
				continue
			
			if not disablePredictor:
				chance = 1
				for game in games:
					games = games[-2:]
					chance *= (1 - (1/33 + (32/33)*(.01 + .99*(1 - 1/game))))

				for game in rgames:
					if game > 2:
						streak[0] += 1
					else:
						streak[1] += 1

				if streak[0] > streak[1]:
					uiprint("Winning streak detected.", "good")
				else:
					uiprint("Losing streak detected", "bad")

				while True:
					request = requests.get("https://bfpredictor.repl.co/multiplier", 
											data={"key": key, 
												  "average": avg,
												  "multiplier": self.multiplier, 
												  "chance": chance
											}
										)

					if request.status_code == 403:
						uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/blox", "error")
						input("Press enter to exit >> ")
						browser.close()
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
				self.updateMultiplier(round(prediction, 2) )


			
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

			uiprint(f"Placing bet with {betamount} Robux on {prediction}x multiplier")
			if self.webhook == None:
				pass
			else:
				sendwebhookmsg(self.webhook, f"Betting {betamount} Robux at {round(prediction,2)}x\n{round(balance-betamount,2)} Robux Left", f"Betting {betamount} Robux ", 0x903cde, f"")
				sendwebhookmsg(self.webhook,f"Average Crash : {round(avg,2)}\nMultiplier Set to : {multiplier}\n Accuracy on last crash : {accuracy}%","Round Predictions", 0xaf5ebd, f"")
			try:
				browser.execute_script("arguments[0].click();", browser.find_element(By.CLASS_NAME, "button_button__eJwei.button_primary__mdLFG.gameBetSubmit"))
			except Exception as e:
				print(e)
				try:
					browser.find_element(By.CSS_SELECTOR, ".button.button_button__eJwei.button_primary__mdLFG.gameBetSubmit").click()
				except:
					pass
if __name__ == "__main__":
	main()
