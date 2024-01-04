from termcolor import cprint
import os


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
	uiprint("Enter multiplier")
	multiplier = float(input(">> "))
	uiprint("Enter bet amount")
	betamount = float(input(">> "))
	uiprint("Enter tax percent (Enter 0 if there's no tax)")
	tax = float(input(">> "))/100
	uiprint("Enter amount of games")
	games = int(input(">> "))

	if not tax:
		chance = (1/33 + (32/33)*(.01 + .99*(1 - 1/multiplier)))
	else:
		chance = 1/multiplier
	
	e = ((( (multiplier-1) * betamount * 1-tax) * (1 - chance)) + (-betamount * chance)) * games
	uiprint(f"If it says you'll lose negative robux that means you'll make profit", "warning")
	uiprint(f"In {games} games expect to lose R$ {round(e, 2)*-1}")
	print("Press enter to retry")
	input(">> ")
	os.system("cls")
	


	