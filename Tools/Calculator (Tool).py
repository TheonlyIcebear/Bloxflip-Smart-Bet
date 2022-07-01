from termcolor import cprint
import os


def uiprint(message, color="cyan"):
	print("[ ", end="")
	cprint("AUTOBET", color, end="")
	print(" ] ", end="")
	cprint(message, color)


while True:
	os.system("")
	uiprint("Enter bet amount")
	betamount = float(input(">> "))
	uiprint("Enter multiplier")
	multiplier = float(input(">> "))
	uiprint("Enter your balance")
	balance = float(input(">> "))

	totalbet = 1
	count = 0


	while True:
		count += 1
		betamount *= 2
		totalbet += betamount
		if totalbet > balance:
			uiprint(f"You can lose {count} games in a row losing before getting cleaned.")
			chance = (((1/33 + (32/33)*(.01 + .99*(1 - 1/multiplier))))**count)*100
			uiprint(f"There's a {chance:.20f}% chance of you getting cleaned before this chance decreases even more.")
			uiprint(f"Or about the same change of a game crashing at {100/chance}")
			print("Press enter to retry")
			input(">> ")
			os.system("cls")
			break