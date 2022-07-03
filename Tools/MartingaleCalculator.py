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
	uiprint("Enter bet amount")
	betamount = float(input(">> "))
	uiprint("Enter multiplier")
	multiplier = float(input(">> "))
	uiprint("Enter your balance")
	balance = float(input(">> "))
	chance, count = getGames(balance)
	

	uiprint(f"You can lose {count} games in a row losing before getting cleaned.")
	chance = 1-(1-((1/33 + (32/33)*(.01 + .99*(1 - 1/multiplier))) **count) )**(200/count)
	uiprint(f"There's around a {chance*100:.20f}% chance of you getting cleaned in 200 games")
	uiprint(f"Or about the same chance of a game crashing at {1/chance}")
	
	print("Press enter to retry")
	input(">> ")
	os.system("cls")
	


	