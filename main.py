#!/usr/bin/env python -W ignore::DeprecationWarning

import seleniumrequests, websockets, threading, requests, asyncio, base64, json, time, os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from termcolor import cprint
from zipfile import *


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

		try:
			test = json.load(open("config.json", "r+"))
			test["multiplier"]
			test["authorization"]
			test["games_averaged"]
		except:
			uiprint("Invalid data inside JSON file. Redownload from github", "error")
			time.sleep(1.6)
			exit()


		with open("config.json", "r+") as data:
			config = json.load(data)
			try:
				self.multiplier = float(config["multiplier"])
			except:
				uiprint("Invalid multipler inside JSON file. Must be valid number", "error")
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
			browser.implicitly_wait(10)
			if "DDoS" in browser.page_source:
				browser.implicitly_wait(15)


			elemnts = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')
			
			elemnts[0].send_keys(f"{Keys.BACKSPACE}")
			elemnts[0].send_keys(f"{self.betamount}")


			elemnts[1].send_keys(f"{Keys.BACKSPACE}")
			elemnts[1].send_keys(f"{self.multiplier}")


	def ChrashPoints(self):
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument('window-size=1920x1080')
		options.add_argument("disable-gpu")
		
		browser = webdriver.Chrome('chromedriver.exe', chrome_options=options)
		browser.get("https://rest-bf.blox.land/games/crash")

		average = self.average
		history = None
		sent = False
		
		while True:
			webdriver.refresh()
			data = browser.page_source.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', "").replace("</pre></body></html>", "")
			games = json.loads(data)
			if games["current"]["status"] == 2 and not sent:
				sent = True
				previd = games["current"]["_id"]
				yield ["game_start", games["history"][0]["crashPoint"]]
			elif games["current"]["status"] == 4:
				sent = False
			if not history == games["history"]:
				history = games["history"]
				yield ["history", [float(crashpoint["crashPoint"]) for crashpoint in history[:average] ]]
			time.sleep(1)

			
	def sendBets(self): # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("If the program doesn't say anything after this point the authorization token is invalid", "warning")
		uiprint("Press Ctrl + C to exit")

		try:

			try:
				self.crashpoints
			except:
				self.crashpoints = []

			multiplier = self.multiplier
			betamount = self.betamount
			browser = self.browser
			average = self.average
			winning = 0
			losing = 0

			for game in self.ChrashPoints():
				if game[0] == "history":
					self.crashpoints = game[1]
					games = self.crashpoints
					avg = sum(games)/len(games)
					uiprint(f"Average Crashpoint: {avg}")

					for crashpoint in games:
						if crashpoint >= multiplier:
							winning += 1
						else:
							losing += 1

					percent = winning/(winning+losing)*100
					uiprint(f"{percent}% of Games Above {multiplier}")
					uiprint(f"{(1/(multiplier-1))/(1/(multiplier-1)+1)*100}% needed to make profit")

				elif game[0] == "game_start":
					uiprint("Game Starting...")
					try:
						percent
					except:
						continue
					if percent >= (1/(multiplier-1))/(1/(multiplier-1)+1)*100:
						uiprint(f"Winning streak detected.", "good")
						time.sleep(1.5)
						uiprint(f"Placing bet for {multiplier}x")
						browser.find_element_by_css_selector(".MuiButtonBase-root.MuiButton-root.MuiButton-contained.jss144.MuiButton-containedPrimary").click()
					else:
						uiprint(f"Losing streak detected.", "bad")


		except KeyboardInterrupt:
			uiprint("Exiting program.")
			exit()

if __name__ == "__main__":
	main()
