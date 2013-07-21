from copy import copy
class GamePlayer:
    def __init__(self):
        self.food = 0.0
        self.timesHunted = 0.0
        self.timesSlacked = 0.0
        self.player = None

    def GetReputation(self):
    	if ( 0 == self.timesHunted and 0 == self.timesSlacked ):
    		return 0
    	else:
    		return self.timesHunted/(self.timesHunted + self.timesSlacked)

    def IsDead(self):
    	return (self.food <= 0)

    def Print(self):
        print   self.player.name +":" + \
                "\n\tFood:          " + str(self.food) + \
                "\n\tTimes Hunted:  " + str(self.timesHunted) + \
                "\n\tTimes Slacked: " + str(self.timesSlacked) + \
                "\n\tReputation:    " + str(self.GetReputation()) + \
                "\n"
