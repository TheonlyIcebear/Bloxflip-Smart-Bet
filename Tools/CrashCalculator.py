from termcolor import cprint
import os


def uiprint(message, color="cyan"):
	print("[ ", end="")
	cprint("AUTOBET", color, end="")
	print(" ] ", end="")
	cprint(message, color)


def getGames(balance):
	global betamount
	totalbet = 1
	count = 0
	while True:
		count += 1
		betamount *= 2
		totalbet += betamount
		if totalbet > balance:
			chance = (1/33 + (32/33)*(.01 + .99*(1 - 1/multiplier)))**count
			return [chance, count]




while True:
	os.system("")
	uiprint("Enter multiplier")
	multiplier = float(input(">> "))
	

	uiprint(f"There's a {(1 - (1/33 + (32/33)*(.01 + .99*(1 - 1/multiplier))))*100}% chance of it crashing at or above {multiplier}")
	
	print("Press enter to retry")
	input(">> ")
	os.system("cls")
	


	