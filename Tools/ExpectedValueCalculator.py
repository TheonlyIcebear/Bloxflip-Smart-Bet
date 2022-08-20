from termcolor import cprint
import os


def uiprint(message, color="cyan"):
	print("[ ", end="")
	cprint("AUTOBET", color, end="")
	print(" ] ", end="")
	cprint(message, color)



while True:
	os.system("")
	uiprint("Enter multiplier")
	multiplier = float(input(">> "))
	uiprint("Enter bet amount")
	betamount = float(input(">> "))
	uiprint("Enter amount of games")
	games = float(input(">> "))

	chance = (1/33 + (32/33)*(.01 + .99*(1 - 1/multiplier)))
	
	e = ((( (multiplier-1) * betamount) * (1 - chance)) + (-betamount * chance)) * games
	uiprint(f"In {games} games expect to lose R$ {round(e, 2)}")
	print("Press enter to retry")
	input(">> ")
	os.system("cls")
	


	