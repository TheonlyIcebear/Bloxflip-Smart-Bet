#!/usr/bin/env python -W ignore::DeprecationWarning

import websockets, threading, asyncio, base64, json, time, os
from termcolor import cprint
class main:
	def __init__(self):
		self.crashPoints = None
		self.target = None
		self.multiplier = 0
		self.chance = 0
		os.system("")
		self.getConfig()
		try:
		  asyncio.get_event_loop().run_until_complete(self.sendBets())
		except DeprecationWarning:
		  pass
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
			json.load(open("config.json", "r+"))
		except json.decoder.JSONDecodeError:
			uiprint("Invalid data inside JSON file. Redownload from github", "error")
			exit()
		with open("config.json", "r+") as data:
			config = json.load(data)
			try:
				self.multiplier = float(config["multiplier"])
				self.chance = 100/self.multiplier/100
				uiprint(f"Chance for this multiplier (Per game)%: {self.chance*100}")
			except:
				uiprint("Invalid multipler inside JSON file. Must be valid number", "error")
				exit()
			try:
				self.target = float(config["chance"]/100)
			except:
				uiprint("Invalid chance inside JSON file. Must be valid number", "error")
				exit()

			try:
				uiprint("Too little or too many games averaged will make the guesses innaccurate. The more the longer it'll take", "warning")
				self.average = int(config["games_averaged"])
			except:
				uiprint("Invalid amount of games to be averaged inside JSON file. Must be valid number", "error")
				exit()

			try:
				self.auth = config["authorization"]
			except:
				uiprint("Invalid authorization inside JSON file. Enter your new authorization from BloxFlip", "error")
				exit()

			try:
				self.betamount = float(config["bet_amount"])
			except:
				uiprint("Invalid bet amount inside JSON file. Must be valid number", "error")
				exit()

	async def sendBets(self): # Actually compare the user's chances of winning and place the bets
		headers = {
				"Accept-Encoding": "gzip, deflate, br",
				"Accept-Language": "en-US,en;q=0.9",
				"Cache-Control": "no-cache",
				"Connection": "Upgrade",
				"Host": "sio-bf.blox.land",
				"Origin": "https://bloxflip.com",
				"Pragma": "no-cache",
				"Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
				"Sec-WebSocket-Key": "C6BOGNpZQXsVOiOX50Znog==",
				"Sec-WebSocket-Version": "13",
				"Upgrade": "websocket",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
			}
		uiprint = self.print
		uiprint("If the program doesn't say anything after this point the authorization token is invalid", "warning")
		uiprint("Press Ctrl + C to exit")
		while True:
			try:
				async with websockets.connect("wss://sio-bf.blox.land/socket.io/?EIO=3&transport=websocket", extra_headers=headers) as websocket:
					await websocket.send('''40/crash''')
					await websocket.send(f'''42/crash, ["auth", "{self.auth}"]''')
					uiprint("Connected")
					try:
						self.crashpoints
					except:
						self.crashpoints = []

					multiplier = self.multiplier
					betamount = self.betamount
					average = self.average
					target = self.target

					while True:
						try:
						  response = await websocket.recv()
						except:
						  uiprint("Disconnected")
						  break
						try:
						  response = eval(response.replace('42/crash,', ''))
						except:
						  continue

						if response == 3:
							continue
						if isinstance(response, list) and response[0] == "game-end":
							uiprint("Game starting!")
							crashpoint = response[1]["crashPoint"]
							self.crashpoints.append(crashpoint)

							if len(self.crashpoints) > average:
								self.crashpoints.pop(0)

							for crashpoint in self.crashpoints[-average:]:
								if crashpoint >= multiplier:
									if self.chance > 0.5:
										self.chance -= (1-self.chance)
									else:
										self.chance = 1-((1-self.chance)+(self.chance/2))
								else:
									self.chance += (1-self.chance)/2

								if self.chance >= 1:
									self.chance = 0.999
								if self.chance <= 0:
									self.chance = 0.001
							uiprint(f"Current chance: {self.chance*100}%")

							games = len(self.crashpoints[-average:])
							if games >= average and self.chance >= target:
								uiprint(f"Placing bet for {multiplier}x with a {self.chance*100}% chance")
								await websocket.send(f'42/crash,["join-game",{{"autoCashoutPoint": {multiplier*100},"betAmount": {betamount} }}]')
							if not games >= average:
								uiprint(f"Not enough diagnostic data. {average-games} more games needed. Please be patient", "warning")
								uiprint(f"If it's taking too long edit games_averaged inside config.json and restart the program", "warning")
							
							if self.chance*100 >= target:
								uiprint(f"Chance of {multiplier}x is less than {target*100}")

							if len(self.crashpoints[-average:]) == average:
							  avg = sum(self.crashpoints[-average:])/len(self.crashpoints[-average:])
							  uiprint(f"Average: {avg}")
						else:
							await websocket.send('''2''')
					continue
			except websockets.exceptions.InvalidStatusCode:
				continue
			except websockets.exceptions.ConnectionClosedError:
				continue
			except KeyboardInterrupt:
				uiprint("Exiting program.")
				exit()

if __name__ == "__main__":
	main()
