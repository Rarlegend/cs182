import random, util, time

class qAgent():
    def __init__ (self, actionFn = None, numTraining=100000, epsilon=0.1, alpha=0.5, gamma=1):
        if (actionFn == None):
            actionFn = lambda state: state.getLegalActions()
        self.actionFn = actionFn
        self.totalRewards = 0
        self.numCorrect = 0
        self.numWrong = 0
        self.numTraining = int(numTraining)
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = gamma
        self.qValues = util.Counter()

    def getQValue(self, state, action):
    	value = self.qValues[(state.getDef(), action)]
    	if (value == 0):
    		print "new state"
    	else:
    		print "old state"
        return value

    def computeActionFromQValues(self, state):
        maxAction = None
        maxVal = 0
        for action in state.getLegalActions():
            qVal = self.getQValue(state, action)
            if qVal > maxVal or maxAction is None:
                maxVal = qVal
                maxAction = action
        return maxAction

    def getAction(self, state):
        legalActions = state.getLegalActions()
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValues(state)

    def update(self, reward, state, action):
        sample = reward
        self.totalRewards += reward
        if (reward < 0):
            self.numWrong += 1
            # self.totalRewards -= 1
        else:
            self.numCorrect += 1
            # self.totalRewards += 1
        self.alpha = float(1 - (float(self.numCorrect + self.numWrong) / float(self.numTraining)))
        addVal = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * sample
        self.qValues[(state.getDef(), action)] = addVal

    def getPercentCorrect(self):
        return float(self.numCorrect) / float(self.numCorrect + self.numWrong)

    def getTotalRewards(self):
        return self.totalRewards

    def finish(self):
        print "DONE"
        print self.totalRewards

