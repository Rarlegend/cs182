import random, util, time
import copy
import gradientParser


#bucket ranges for different metrics
buckets = dict()
for i in range(55):
	#buckets[i] = [0,-50,-40,-30,-20,-10,10,20,30,40,50,10000000]
	# buckets[i] = [0,10000000]
	buckets[i] = [0,-10,-6,-3,-2,-1,-0.5,0,0.5,1,1.5,2,2.5,3,6,10,10000000]

#take data and put it into buckets defined somewhere else
class state():
	def __init__(self, values):
		data = values[0]
		newPrice = values[2]
		self.data = data
		self.curPrice = values[1]
		self.newPrice = newPrice
		stateDef = []
		#print data
		#print values
		#place values into buckets
		for i in range(0, len(data)):
			bucketRanges = buckets[i]
			dataVal = data[i]
			if (dataVal == None):
				stateDef += [0]
			else:
				for j in range(1,len(bucketRanges)):
					if (data[i] < bucketRanges[j]):
						stateDef += [j]
						break
		self.stateDef = tuple(stateDef)
		#print (self.stateDef)
	def getScore(self):
		if (self.newPrice == None or self.curPrice == None):
			return 0.0
		priceChange = float(self.newPrice - self.curPrice) 
		return priceChange
	#-1 = predict lower price, 1 = predict higher price
	def getLegalActions(self):
		return [-1,1]
	def getDef(self):
		return self.stateDef

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
		self.inTesting = False
		self.testRewards = 0
		self.testCorrect = 0
		self.testWrong = 0

	def getQValue(self, state, action):
		value = self.qValues[(state.getDef(), action)]
		# print action
		# if (value == 0):
		# 	print "new state"
		# 	print action
		# 	print state.getDef()
		# else:
		# 	print "old state"
		return value

	def computeActionFromQValues(self, state):
		maxAction = None
		maxVal = 0
		actions = state.getLegalActions()
		for action in actions:
			# print action
			qVal = self.getQValue(state, action)
			if qVal > maxVal or maxAction is None:
				maxVal = qVal
				maxAction = action
		if (maxVal == 0):
			return random.choice(actions)
		else:
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
		# print "add"
		# print addVal
		self.qValues[(state.getDef(), action)] = addVal

	def getPercentCorrect(self):
		if (self.inTesting):
			return float(self.testCorrect) / float(self.test + self.testWrong)
		else:
			return float(self.numCorrect) / float(self.numCorrect + self.numWrong)

	def getTotalRewards(self):
		if (self.inTesting):
			return self.testRewards
		else:
			return self.totalRewards

	def finish(self):
		print ("DONE")
		print (self.totalRewards)

	def setTestingOn(self):
		self.epsilon = 0.0    
		self.alpha = 0.0      

# def runInnerLoop(selectedKeys):
# 	agent = qAgent()
# 	reward = 0
# 	correct = 0
# 	# open data row by row to avoid memory overflow
# 	fname = 'data_cleaned.csv'
# 	with open(fname, 'r+') as f:
# 		# this reads in one line at a time from stdin
# 		date_previous = None 
# 		ticker_previous = None

# 		observation = {}
# 		observationPrevious = {}
# 		isFirstObservation = True

# 		lineo = 0

# 		for i, line in enumerate(f):
# 			#print line
# 			fList = line.split(",")
# 			date = fList[0]
# 			value = float(fList[1])
# 			ticker = str(fList[2])
# 			fundamental = str(fList[3])
# 			lineo += 1
# 			if (lineo == 10000):
# 				break

# 			if (date_previous == None):
# 				date_previous = date
# 			elif (date_previous != date):
# 				if (not isFirstObservation):
# 					#break
# 					observedData = gradientParser.getObservation(observationPrevious, observation, selectedKeys)
# 					curState = state(observedData)
# 					action = agent.getAction(curState)
# 					priceChange = curState.getScore()
# 					reward = action * priceChange
# 					agent.update(reward, curState, action)
# 					reward = agent.getTotalRewards()
# 					correct = agent.getPercentCorrect()
# 				else:
# 					isFirstObservation = False
# 				observationPrevious = copy.deepcopy(observation)
# 				observation = {}
# 				date_previous = date

# 			if (ticker_previous == None):
# 				ticker_previous = ticker
# 			elif (ticker_previous != ticker):
# 				isFirstObservation = True
# 				ticker_previous = ticker

# 			observation[fundamental] = value
# 	return [reward, correct]

def runInnerLoop(selectedKeys):
	agent = qAgent()
	reward = 0
	correct = 0
	# open data row by row to avoid memory overflow
	fname = 'data_ARQ_price.csv'
	with open(fname, 'r+') as f:
		# this reads in one line at a time from stdin
		date_previous = None 
		ticker_previous = None

		observation = {}
		observationPrevious = {}
		isFirstObservation = True

		lineo = 0
		currentPriceDict = dict()
		currentDateList = []

		for i, line in enumerate(f):
			lineo += 1
			if (lineo == 10000):
				break

			fList = line.split(",")
			date = fList[0]
			value = float(fList[1])
			ticker = str(fList[2])
			#add the -1 thing to get rid of newline character
			fundamental = str(fList[3])[:-1]

			if (ticker_previous == None):
				ticker_previous = ticker
			elif (ticker_previous != ticker):
				isFirstObservation = True
				ticker_previous = ticker

			if (fundamental == '"PRICE"'):
				currentDateList.append(date)
				currentPriceDict[hash(date)] = value
			else:
				if (date_previous != date):
					if (not isFirstObservation):
						try:
							index = currentDateList.index(date)
						except:
							index = None
						if (index):
							observation['"PRICE"'] = currentPriceDict[hash(currentDateList[index])]
							if (index + 3 >= len(currentDateList)):
								index = len(currentDateList) - 1
							else:
								index = index + 3
							observation['"PRICENEXT"'] = currentPriceDict[hash(currentDateList[index])]
							observedData = gradientParser.getObservation(observationPrevious, observation, selectedKeys)
							curState = state(observedData)
							action = agent.getAction(curState)
							priceChange = curState.getScore()
							reward = action * priceChange
							agent.update(reward, curState, action)
							reward = agent.getTotalRewards()
							correct = agent.getPercentCorrect()
					else:
						isFirstObservation = False
					observationPrevious = copy.deepcopy(observation)
					observation = {}
					date_previous = date

			observation[fundamental] = value

	return [reward, correct, agent]
