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
			exit()
		except Exception as e:
			open("errors.txt", "w+").close()
			now = time.localtime()
			logging.exception(f'A error has occured at {time.strftime("%H:%M:%S %I", now)}')
			self.print("An error has occured check logs.txt for more info", "error")
			time.sleep(2)
			raise
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


	def getBalance(self):
		uiprint = self.print
		balance = None
		browser = self.browser

		classnames = [".MuiBox-root.jss227.jss44", ".MuiBox-root.jss220.jss44", ".MuiBox-root.jss102.jss44", ".MuiBox-root.jss226.jss44", ".MuiBox-root.jss221.jss44"]
		for possibleclass in classnames:
			try:
				balance = float(browser.find_element_by_css_selector(possibleclass).text.replace(',', ''))
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


			try:
				self.stop =  float(config["auto_stop"])
			except:
				uiprint("Invalid auto stop amount inside JSON file. Must be a valid number", "error")
				time.sleep(1.6)
				exit()


			try:
				self.stoploss =  float(config["stop_loss"])
			except:
				uiprint("Invalid auto stop_loss inside JSON file. Must be a valid number", "error")
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

			options = webdriver.ChromeOptions()
			options.add_experimental_option('excludeSwitches', ['enable-logging'])
			try:
				self.browser = webdriver.Chrome("chromedriver.exe", chrome_options=options)
			except selenium.common.exceptions.SessionNotCreatedException:
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
			data = browser.page_source.replace('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', "").replace("</pre></body></html>", "")
			try:
				games = json.loads(data)
			except json.decoder.JSONDecodeError:
				uiprint("Blocked by ddos protection. If there's a captcha solve it.", "error")
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

			
	def sendBets(self): # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("Betting started. Press Ctrl + C to exit")


		try:
			self.crashpoints
		except:
			self.crashpoints = []


		multiplier = self.multiplier
		betamount = self.betamount
		stoploss = self.stoploss
		browser = self.browser
		average = self.average
		stop = self.stop
		winning = 0
		losing = 0

		for game in self.ChrashPoints():
			uiprint("Game Starting...")
			balance = self.getBalance()


			uiprint(f"Your balance is {balance}")
			if balance < betamount:
				uiprint("You don't have enough robux to continue betting.", "error")
				exit()
			elif balance > stop:
				uiprint("Auto Stop goal reached. Betting has stopped.", "good")
				uiprint("If the program is reaching the goal instantly that likely means your balance is already above the auto_stop amount.", "warning")
				uiprint("To fix this simply increase the number to a number higher than your current balance.", "warning")
				input("Press enter to exit >> ")
				browser.close()
				exit()
			elif balance < stoploss:
				uiprint(f"Balance is below stop loss. All betting has stopped.", "bad")
				input("Press enter to exit >> ")
				browser.close()
				exit()
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
				if losing == 0:
					losing = 1
				if winning == 0:
					winning = 1

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
					uiprint(f"Placing bet for {multiplier}x")
					time.sleep(2)
					try:
						browser.find_element_by_css_selector(".MuiButtonBase-root.MuiButton-root.MuiButton-contained.jss142.MuiButton-containedPrimary").click()
					except:
						browser.find_element_by_css_selector(".MuiButtonBase-root.MuiButton-root.MuiButton-contained.jss143.MuiButton-containedPrimary").click()
				else:
					uiprint(f"Losing streak detected.", "bad")

if __name__ == "__main__":
	main()