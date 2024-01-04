from termcolor import cprint
import cloudscraper, os


def uiprint(message="", option=None): # print the ui's text with
	print("[ ", end="")
	if not option:
		cprint("AUTOBET", "cyan", end="")
		print(" ] ", end="")
		if message:
			cprint(message, "cyan")
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



while True:
	os.system("")
	uiprint("Enter case id")
	caseid = input(">> ")
	uiprint("Enter amount of games")
	games = float(input(">> "))

	scraper = cloudscraper.create_scraper()

	data = scraper.get(f"https://api.bloxflip.com/games/community-cases/{caseid}").json()
	if not data["success"]:
		uiprint("Invalid Case Id!", "error")

	items = data["cases"][0]["items"]
	price = data["cases"][0]["price"]

	e = 0

	for item in items:
		value = item["value"]
		chance = item["winningChance"]
		if value > price:
			e += (value-price) * chance
		elif value < price:
			e += (value-price) * chance

	uiprint(f"If it says you'll lose negative robux that means you'll make profit", "warning")
	uiprint(f"In {games} games it's most likely that you'll to lose R$ {round(e, 2)*-1}")
	print("Press enter to retry")
	input(">> ")
	os.system("cls")
	


	