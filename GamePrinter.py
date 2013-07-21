def PrintM(gameRound) :
	print "Value of 'm' for this round: " + str(gameRound.m)

def PrintGameRound(gameRound) :
	gameRound.PrintM()
	for gamePlayer in gameRound.gamePlayerList :
		gamePlayer.Print()

def PrintGameRoundList(gameRoundList) :
	roundCounter = 1
	for gameRound in gameRoundList :
		roundStartString = "************* ROUND " + str(roundCounter) + " *************"
		print roundStartString
		PrintGameRound(gameRound)
		roundCounter += 1
		print "*" * len(roundStartString)
		print "\n\n\n\n"