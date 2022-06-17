#!/usr/bin/env python -W ignore::DeprecationWarning

import subprocess, selenium, requests, logging, base64, json, time, os
from selenium.webdriver.common.keys import Keys
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
				self.betamount = float(config["bet_amount"])
			except:
				uiprint("Invalid bet_amount inside JSON file. Must be valid number", "error")
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
				uiprint("Invalid auto_restart boolean inside JSON file. Must be True or False", "error")
				time.sleep(1.6)
				exit()

			if not type(self.restart) == bool:
				uiprint("Invalid auto_restart boolean inside JSON file. Must be true or false 1", "error")
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


			elements = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')
			if not elements:
				uiprint("Blocked by DDoS protection. Solve the captcha on the chrome window to continue.")
			while not elements:
				elements = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')


			try:
				balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss227.jss44").text.replace(',', ''))
			except selenium.common.exceptions.NoSuchElementException:
				try:
					balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss220.jss44").text.replace(',', ''))
				except selenium.common.exceptions.NoSuchElementException:
					try:
						balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss102.jss44").text.replace(',', ''))
					except selenium.common.exceptions.NoSuchElementException:
						try:
							balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss226.jss44").text.replace(',', ''))
						except:
							try:
								balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss221.jss44").text.replace(',', ''))
							except:
								uiprint("Invalid authorization. Make sure you copied it correctly, and for more info check the github", "bad")
								time.sleep(1.7)
								browser.close()
								exit()


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
			if games["current"]["status"] == 2 and not sent:
				sent = True
				previd = games["current"]["_id"]
				yield ["game_start", games["history"][0]["crashPoint"]]
			elif games["current"]["status"] == 3:
				sent = False
			if not history == games["history"]:
				history = games["history"]
				yield ["history", [float(crashpoint["crashPoint"]) for crashpoint in history[:average] ]]
			time.sleep(0.01)

	def updateBetAmount(self, amount):
		browser = self.browser
		elemnts = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')
		for _ in range(10):
			elemnts[0].send_keys(f"{Keys.BACKSPACE}")
		elemnts[0].send_keys(f"{amount}")

	def sendBets(self): # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("Betting started. Press Ctrl + C to exit")


		multiplier = self.multiplier
		betamount = self.betamount
		stoploss = self.stoploss
		browser = self.browser
		average = self.average
		restart = self.restart
		stop = self.stop
		lastgame = None
		winning = 0
		losing = 0


		for game in self.ChrashPoints():
			if game[0] == "history":
				games = game[1]
				avg = sum(games)/len(games)
				uiprint(f"Average Crashpoint: {avg}")

			if game[0] == "game_start":
				uiprint("Game Starting...")
				try:
					balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss227.jss44").text.replace(',', ''))
				except selenium.common.exceptions.NoSuchElementException:
					try:
						balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss220.jss44").text.replace(',', ''))
					except selenium.common.exceptions.NoSuchElementException:
						try:
							balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss102.jss44").text.replace(',', ''))
						except selenium.common.exceptions.NoSuchElementException:
							try:
								balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss226.jss44").text.replace(',', ''))
							except:
								try:
									balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss221.jss44").text.replace(',', ''))
								except:
									uiprint("Invalid authorization. Make sure you copied it correctly, and for more info check the github", "bad")
									time.sleep(1.7)
									browser.close()
									exit()


				try:
					games[0]
				except:
					continue
				uiprint(f"Your balance is {balance}")
				if balance < betamount:
					uiprint("You don't have enough robux to continue betting.", "error")
					if not balance < self.betamount and not restart:
						input(f"Press enter to restart betting with {self.betamount} robux")
						betamount = self.betamount
					elif not balance < self.betamount and restart:
						uiprint("Overwritten: Auto Restart is enabled", "warning")
						betamount = self.betamount
					else:
						input("Press enter to exit >> ")
						browser.close()
						exit()
				elif balance > stop:
					uiprint("Auto Stop goal reached. Betting has stopped.", "good")
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
					input("Press enter to exit >> ")
					browser.close()
					exit()
				elif balance-betamount < stoploss:
					uiprint(f"Resetting bet amount to {self.betamount}. If game is lost balance will be under stop loss", "warning")
					betamount = self.betamount
				

				uiprint(f"Placing bet with {betamount} Robux on {multiplier}x multiplier")
				if lastgame:
					lastgame = game[1]
					if lastgame < multiplier:
						betamount = betamount*2
						self.updateBetAmount(betamount)
						uiprint(f"Lost game. Increasing bet amount to {betamount}", "bad")
					else:
						betamount = self.betamount
						self.updateBetAmount(betamount)
						uiprint(f"Won game. Lowering bet amount to {betamount}", "good")
				else:
					lastgame = games[0]
				time.sleep(2)
				try:
					browser.find_element_by_css_selector(".MuiButtonBase-root.MuiButton-root.MuiButton-contained.jss142.MuiButton-containedPrimary").click()
				except:
					browser.find_element_by_css_selector(".MuiButtonBase-root.MuiButton-root.MuiButton-contained.jss143.MuiButton-containedPrimary").click()
if __name__ == "__main__":
	main()