#!/usr/bin/env python -W ignore::DeprecationWarning

import requests, base64, json, time, os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from termcolor import cprint
from zipfile import *
from sys import exit


class main:
	def __init__(self):
		self.crashPoints = None
		self.multiplier = 0
		os.system("")
		self.getConfig()
		try:
		  self.sendBets()
		except KeyboardInterrupt:
			self.print("Exiting program.")
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


	def getConfig(self): # Get configuration from config.json file
		uiprint = self.print
		print("[", end="")
		cprint(base64.b64decode(b'IENSRURJVFMg').decode('utf-8'), "cyan", end="")
		print("]", end="")
		print(base64.b64decode(b'IE1hZGUgYnkgSWNlIEJlYXIjMDE2Nw==').decode('utf-8'))
		time.sleep(3)
		self.clear()

		with open("config.json", "r+") as data:
			config = json.load(data)
			try:
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
					uiprint("Too many games averaged. Must be 35 or less games", "error")
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
				uiprint("Invalid bet amount inside JSON file. Must be valid number", "error")
				time.sleep(1.6)
				exit()


			latest_version = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_100").text
			download = requests.get(f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_win32.zip")

			if not os.path.exists("chromedriver.exe"):
				uiprint("Chromedriver not insatlled", "bad")
				uiprint("Installing chrome driver...", "warning")


				with open("chromedriver.zip", "wb") as zip:
					zip.write(download.content)


				with ZipFile("chromedriver.zip", "r") as zip:
					zip.extract("chromedriver.exe")
				os.remove("chromedriver.zip")

			options = webdriver.ChromeOptions()
			options.add_experimental_option('excludeSwitches', ['enable-logging'])
			self.browser = webdriver.Chrome("chromedriver.exe", chrome_options=options)
			browser = self.browser
			browser.get("https://bloxflip.com/crash") # Open bloxflip
			browser.execute_script(f'''localStorage.setItem("_DO_NOT_SHARE_BLOXFLIP_TOKEN", "{self.auth}")''') # Login with authorization
			browser.execute_script(f'''window.location = window.location''')


			elements = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')
			if not elements:
				uiprint("Blocked by DDoS protection. Solve the captcha on the chrome window to continue.")
			while not elements:
				elements = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')
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
			data = browser.page_source.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', "").replace("</pre></body></html>", "")
			try:
				games = json.loads(data)
			except json.decoder.JSONDecodeError:
				uiprint("Blocked by ddos protection. If there's a captcha solve it.", "error")
				time.sleep(20)
				exit()
			if games["current"]["status"] == 4 and not sent:
				sent = True
				previd = games["current"]["_id"]
				yield ["game_start", games["history"][0]["crashPoint"]]
			elif games["current"]["status"] == 3:
				sent = False
			if not history == games["history"]:
				history = games["history"]
				yield ["history", [float(crashpoint["crashPoint"]) for crashpoint in history[:average] ]]
			time.sleep(1)

	def updateBetAmount(self, amount):
		browser = self.browser
		elemnts = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')
		for _ in range(10):
			elemnts[0].send_keys(f"{Keys.BACKSPACE}")
		elemnts[0].send_keys(f"{amount}")

	def sendBets(self): # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("Betting started. Press Ctrl + C to exit")

		try:

			multiplier = self.multiplier
			betamount = self.betamount
			browser = self.browser
			average = self.average
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
						balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss227.jss44").text)
					except:
						balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss220.jss44").text)
					uiprint(f"Your balance is {balance}")
					if balance < betamount:
						uiprint("You don't have enough robux to continue betting.", "error")
						if not balance < self.betamount:
							input(f"Press enter to restart betting with {self.betamount} robux")
							betamount = self.betamount
						else:
							input("Press enter to exit")
							exit()
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
							uiprint(f"Won game. Lowering bet amount to {betamount}")
					else:
						lastgame = games[0]
					browser.find_element_by_css_selector(".MuiButtonBase-root.MuiButton-root.MuiButton-contained.jss142.MuiButton-containedPrimary").click()


		except KeyboardInterrupt:
			uiprint("Exiting program.")
			exit()

if __name__ == "__main__":
	main()
