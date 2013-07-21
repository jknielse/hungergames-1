from __future__ import division, print_function
import random
from copy import copy
from copy import deepcopy
from GamePlayer import GamePlayer
from GameRound import GameRound

# I have no idea what these numbers should be yet
MIN_ROUNDS = 300
AVERAGE_ROUNDS = 1000

def payout(*args):
    #Times 3 because this calculates one person's share
    return args.count('h') * 3

def loss(huntOrSlack):
	if huntOrSlack == 's':
		return -2
	elif huntOrSlack == 'h':
		return -6
	else:
		raise Exception('huntOrSlack was not one of \'s\' or \'h\'\nDo you even lift bro?')

def add(x,y):
	return x + y



    
class Game(object):    
    def __init__(self, players, verbose=True):
        self.max_rounds = MIN_ROUNDS + int(random.expovariate(1/(AVERAGE_ROUNDS - MIN_ROUNDS)))
        self.round = 0
        self.gameRoundList = []

        self.gamePlayerList = []
        #For each player, we're going to construct a "GamePlayer" object to help us keep
        #track of food and reputation and whatnot.
        for eachPlayer in players:
        	newGamePlayer = GamePlayer()
        	#Start the players off with 300*(P - 1) food
        	newGamePlayer.food = (len(players) - 1) * 300
        	newGamePlayer.player = eachPlayer

        	self.gamePlayerList += [newGamePlayer]
    
    @property
    def P(self):
        return len(self.gamePlayerList)
        
    def calculate_m(self):
        try:
            return random.randrange(1, self.P*(self.P-1))
        except ValueError:
            # m stops existing for 2 players
            return 3
            
        
    def play_round(self):
        #The first step of a round is to pit every player against every other player and see how they fare
        self.round += 1
        m = self.calculate_m()
        
        shuffledPlayerList = list(self.gamePlayerList)
        random.shuffle(shuffledPlayerList)

        resultList = []

        for eachGamePlayer in shuffledPlayerList:
        	otherGamePlayers = list(shuffledPlayerList)
        	otherGamePlayers.remove(eachGamePlayer)

        	result = eachGamePlayer.player.hunt_choices( self.round, \
														 eachGamePlayer.food, \
														 eachGamePlayer.GetReputation(), \
														 m, \
														 [player.GetReputation() for player in otherGamePlayers])
        	resultList += [result]
        	#It may be tempting to update the game player's reputation right now, but that would be visable to the other players,
        	#so we must do this *after* the hunt_choices stage

        for eachGamePlayerIndex in range(len(shuffledPlayerList)) :
        	shuffledPlayerList[eachGamePlayerIndex].timesHunted += resultList[eachGamePlayerIndex].count('h')
        	shuffledPlayerList[eachGamePlayerIndex].timesSlacked += resultList[eachGamePlayerIndex].count('s')


        #Now that we have the results, we need to construct the earnings lists for each player.
        #To do this, we're going to populate a P*P matrix with the results of their interactions:
        earningsMatrix = []

        #So that we don't run into out of range exceptions, I'm just going to pre-set all of the values in earningsMatrix:
        for oneplayer in range(len(shuffledPlayerList)):
        	earningsMatrix.append([])
        	for otherplayer in range(len(shuffledPlayerList)):
        		earningsMatrix[oneplayer].append('')

        currentPlayerIndex = 0
        for eachGamePlayer in shuffledPlayerList:
        	rivalPlayerIndex = 0
        	for eachRivalPlayer in shuffledPlayerList:
        		if eachGamePlayer != eachRivalPlayer:
        			resultIndex = rivalPlayerIndex
        			if rivalPlayerIndex > currentPlayerIndex:
        				resultIndex -= 1
        			earningsMatrix[currentPlayerIndex][rivalPlayerIndex] += '' #resultList[currentPlayerIndex][resultIndex]
        			earningsMatrix[rivalPlayerIndex][currentPlayerIndex] += '' #resultList[currentPlayerIndex][resultIndex]
        		rivalPlayerIndex += 1
        	currentPlayerIndex += 1

        #Now that the results have been put into an earning matrix, we're going to map that into earning lists, and pass those
        #lists to the player objects (i.e. figure out what we need to pass to hunt_outcomes())
        #While we're at it, we're gonna keep track of the number of people who hunted in order to determine the award food
        #in the next step.
        totalFoodProduced = 0

        currentPlayerIndex = 0
        for eachGamePlayer in shuffledPlayerList:
        	del earningsMatrix[currentPlayerIndex][currentPlayerIndex]
        	huntOutcomes = map(payout,earningsMatrix[currentPlayerIndex])
        	foodProducedThisRound = reduce(add, huntOutcomes)
        	totalFoodProduced += foodProducedThisRound
        	#Adds this player's share of the food produced from the hunt
        	eachGamePlayer.food += totalFoodProduced
        	#This will return a negative number btw:
        	foodExpendedByThisPlayer = reduce(add , map(loss, resultList[currentPlayerIndex]))

        	#Removes the food expended by this player
        	eachGamePlayer.food += foodExpendedByThisPlayer

        	eachGamePlayer.player.hunt_outcomes(huntOutcomes) 
        	currentPlayerIndex += 1
        #The /6 is because people produce 6 food every hunt. Hence, the total number of hunters must be the food produced
        #divided by 6.
        totalNumberOfHunters = totalFoodProduced/6

        foodAward = 0
        if totalNumberOfHunters >= m:
        	foodAward = 2 * (self.P - 1)

        for eachGamePlayer in shuffledPlayerList:
        	eachGamePlayer.food += foodAward
        	eachGamePlayer.player.round_end(foodAward,m,totalNumberOfHunters)

        #The penultimate step in this procedure is to remove players that have died:
        for eachGamePlayer in shuffledPlayerList:
        	if eachGamePlayer.IsDead():
        		self.gamePlayerList.remove(eachGamePlayer)

        #Finally, we need to construct a GameRound object that we will return to the caller, and
        #then determine if the game has ended:

        gameRound = GameRound()
        gameRound.m = m
        gameRound.gamePlayerList = deepcopy(self.gamePlayerList)
        self.gameRoundList += [gameRound]

        #If everyone except one person is dead, or if we've hit the last round, then
        #the game is over.
        if (len(self.gamePlayerList) <= 1) or (self.round >= self.max_rounds):
        	return False

        self.round += 1
        return True

    def play_game(self):
        
        while self.play_round():
        	pass

        return self.gameRoundList
        