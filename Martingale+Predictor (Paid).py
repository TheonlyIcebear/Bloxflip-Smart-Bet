#!/usr/bin/env python -W ignore::DeprecationWarning

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
			raise
			self.browser.close()
			exit()

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


	def clear(self): # Clear the console
		if os.name == 'nt':
		  os.system("cls")
		else:
		  os.system("clear")


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
		browser = self.browser

		classnames = [".MuiBox-root.jss227.jss44", 
					  ".MuiBox-root.jss220.jss44", 
					  ".MuiBox-root.jss102.jss44", 
					  ".MuiBox-root.jss226.jss44", 
					  ".MuiBox-root.jss221.jss44", 
					  ".MuiBox-root.jss271.jss44", 
					  ".MuiBox-root.jss359.jss44", 
					  ".MuiBox-root.jss221.jss44",
					  ".MuiBox-root.jss233.jss44",
					  ".MuiBox-root.jss226.jss44",
					  ".MuiBox-root.jss247.jss44"]

		for possibleclass in classnames:
			try:
				balance = float(browser.find_element(By.CSS_SELECTOR, possibleclass).text.replace(',', ''))
			except selenium.common.exceptions.NoSuchElementException:
				pass
			except ValueError:
				pass
		if not balance:
			uiprint("Invalid authorization. Make sure you copied it correctly, and for more info check the github", "bad")
			time.sleep(1.7)
			while True:
				pass
			browser.close()
			exit()
		return balance


	def getConfig(self): # Get configuration from data.json file
		uiprint = self.print
		print("[", end="")
		cprint(base64.b64decode(b'IENSRURJVFMg').decode('utf-8'), "cyan", end="")
		print("]", end="")
		print(base64.b64decode(b'IE1hZGUgYnkgSWNlIEJlYXIjMDE2Nw==').decode('utf-8'))
		time.sleep(3)
		self.clear()

		try:
			open("data.json", "r").close()
		except:
			uiprint("data.json file is missing. Make sure you downloaded all the files and they're all in the same folder", "error")

		with open("data.json", "r+") as data:
			try:
				config = json.load(data)
				self.multiplier = float(config["multiplier"])
				if self.multiplier < 2:
					uiprint("Multiplier must be above 2 to make profit.", "error")
					time.sleep(1.6)
					exit()
			except ValueError:
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
				self.sound = config["play_sounds"]
			except:
				uiprint("Invalid play_sounds boolean inside JSON file. Must be true or false", "error")
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


			self.installDriver()
			options = webdriver.ChromeOptions()
			options.add_experimental_option('excludeSwitches', ['enable-logging'])
			try:
				self.browser = webdriver.Chrome("chromedriver.exe", chrome_options=options)
			except selenium.common.exceptions.SessionNotCreatedException:
				try:
					self.installDrier(100)
				except:
					uiprint("Chromedriver version not compatible with current chrome version installed. Update your chrome to continue.", "error")
					uiprint("If your not sure how to update just uninstall then reinstall chrome", "yellow")
					time.sleep(5)
					exit()


			browser = self.browser
			browser.get("https://bloxflip.com/crash") # Open bloxflip
			browser.execute_script(f'''localStorage.setItem("_DO_NOT_SHARE_BLOXFLIP_TOKEN", "{self.auth}")''') # Login with authorization
			browser.execute_script(f'''window.location = window.location''')
			time.sleep(1.5)

			self.getBalance()
			elements = browser.find_elements(By.CSS_SELECTOR, '.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')
			if not elements:
				uiprint("Blocked by DDoS protection. Solve the captcha on the chrome window to continue.")
			while not elements:
				elements = browser.find_elements(By.CSS_SELECTOR, '.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')


			elements[0].send_keys(f"{Keys.BACKSPACE}")
			elements[0].send_keys(f"{self.betamount}")


			elements[1].send_keys(f"{Keys.BACKSPACE}")
			elements[1].send_keys(f"{self.multiplier}")


	def ChrashPoints(self):		
		browser = webdriver.Chrome('chromedriver.exe')
		browser.get("https://rest-bf.blox.land/games/crash")

		average = self.average
		history = None
		uiprint = self.print
		sent = False
		
		while True:
			browser.refresh()
			data = browser.page_source.replace('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', "").replace("</pre></body></html>", "")
			try:
				games = json.loads(data)
			except json.decoder.JSONDecodeError:
				uiprint("Blocked by ddos protection. Solve the captcha to continue.", "error")
				time.sleep(20)
				browser.close()
				exit()
			if not history == games["history"]:
				history = games["history"]
				yield [games["history"][0]["crashPoint"], [float(crashpoint["crashPoint"]) for crashpoint in history[:average]]]
			time.sleep(0.01)


	def playsounds(self, file):
		if self.sound:
			playsound(file)


	def updateBetAmount(self, amount):
		browser = self.browser
		element = browser.find_elements(By.CSS_SELECTOR, '.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')[0]
		for _ in range(10):
			element.send_keys(f"{Keys.BACKSPACE}")
		element.send_keys(f"{amount}")


	def updateMultiplier(self, multiplier):
		browser = self.browser
		element = browser.find_elements(By.CSS_SELECTOR, '.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')[1]
		for _ in range(10):
			element.send_keys(f"{Keys.BACKSPACE}")
		element.send_keys(f"{multiplier}")


	def playsounds(self, file):
		if self.sound:
			playsound(file)


	def sendBets(self): # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("Betting started. Press Ctrl + C to exit")


		multiplier = self.multiplier
		playsounds = self.playsounds
		betamount = self.betamount
		stoploss = self.stoploss
		browser = self.browser
		average = self.average
		restart = self.restart
		maxbet = self.maxbet
		stop = self.stop
		lastgame = None
		bet = self.bet
		key = self.key
		winning = 0
		losing = 0


		for game in self.ChrashPoints():
			uiprint("Game Starting...")
			balance = self.getBalance()

			games = game[1]
			lastgame = game[0]
			avg = sum(games)/len(games)
			uiprint(f"Average Crashpoint: {avg}")


			try:
				if lastgame > prediction:
					betamount = self.betamount
					uiprint(f"Won previous game. lowering bet amount to {betamount}", "good")
					uiprint(f"Accuracy on previous guess: {(1-(abs(multiplier-lastgame))/lastgame)*100}", "yellow")
					self.updateBetAmount(betamount)
					try:
						threading.Thread(target=playsounds, args=('Assets\Won.mp3',)).start()
					except:
						pass
				else:
					betamount *= 2
					uiprint(f"Lost previous game. Increasing bet amount to {betamount}", "bad")
					uiprint(f"Accuracy on previous guess: {(1-(abs(lastgame-multiplier))/multiplier)*100}", "yellow")
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

			chance = 1
			for game in games:
				chance = chance * ((100/game)/100)
			
			request = requests.get("https://predictor.repl.co/multiplier", 
										data={"key": key, 
											  "average": average,
											  "multiplier": self.multiplier, 
											  "chance": chance
										}
									)

			if request.status_code == 403:
				uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/HhwNFRaC", "error")
				input("Press enter to exit >> ")
				browser.close()
				exit()
			elif request.status_code == 500:
				uiprint("Internal server error. Please try again later", "error")
				input("Press enter to exit >> ")
				browser.close()
				exit()
			elif request.status_code == 200:
				prediction = float(request.text)
			else:
				uiprint("Internal server error. Please try again later", "error")
				input("Press enter to exit >> ")
				browser.close()
				exit()




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
			
			if round(multiplier, 2) <= 1:
				uiprint("Cancelling bet this game. As the game will likely crash around 1x.")
				continue

			uiprint(f"Placing bet with {betamount} Robux on {prediction}x multiplier")
			
			try:
				browser.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.jss142.MuiButton-containedPrimary").click()
			except:
				browser.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.jss143.MuiButton-containedPrimary").click()
if __name__ == "__main__":
	main()