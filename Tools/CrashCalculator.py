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
	

	uiprint(f"There's a {(1 - (1/33 + (32/33)*(.01 + .99*(1 - 1/multiplier))))*100}% chance of it crashing at or above {multiplier}")
	print("Press enter to retry")
	input(">> ")
	os.system("cls")
	


	