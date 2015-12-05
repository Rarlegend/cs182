import myownq
import gradientParser
import copy
import random
import util

#bucket ranges for different metrics
buckets = dict()
gradientEpsilon = 0.01
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

agent = myownq.qAgent()
#The function that runs the inner Q-learning
def run():
	initialized = False
	#no price in these keys
	keys = ['"ACCOCI"', '"ASSETS"', '"ASSETSC"', '"ASSETSNC"', '"BVPS"', '"CAPEX"', '"CASHNEQ"', '"COR"', '"CURRENTRATIO"', '"DE"', '"DEBT"', '"DEPAMOR"', '"DILUTIONRATIO"', '"DPS"', '"EBIT"', '"EBITDA"', '"EBT"', '"EPS"', '"EPSDIL"', '"EQUITY"', '"FCF"', '"FCFPS"', '"GP"', '"INTANGIBLES"', '"INTEXP"', '"INVENTORY"', '"LIABILITIES"', '"LIABILITIESC"', '"LIABILITIESNC"', '"NCF"', '"NCFCOMMON"', '"NCFDEBT"', '"NCFDIV"', '"NCFF"', '"NCFI"', '"NCFO"', '"NCFX"', '"NETINC"', '"NETINCCMN"', '"NETINCDIS"', '"PAYABLES"', '"PB"', '"PREFDIVIS"', '"RECEIVABLES"', '"RETEARN"', '"REVENUE"', '"RND"', '"SGNA"', '"SHARESWA"', '"SHARESWADIL"', '"TANGIBLES"', '"TAXEXP"', '"TBVPS"', '"WORKINGCAPITAL"']
	selectedKeys = random.sample(keys, 10)
	selectedKeys += ['"PRICE"']
	remainingKeys = [key for key in keys if key not in selectedKeys]
	hashVal = hash(tuple(selectedKeys))
	fScoreCorrect = dict()
	fScoreRewards = dict()
	previousState = dict()
	visited = []
	maxState = dict()

	for x in range(1,100000):
		#random restarts
		if (x%10000 == 0):
			selectedKeys = random.sample(keys, 10)
			selectedKeys += ['"PRICE"']
			remainingKeys = [key for key in keys if key not in selectedKeys]
			hashVal = hash(tuple(selectedKeys))
			previousState = dict()
			print "RESTART"

		# open data row by row to avoid memory overflow
		fname = 'data_cleaned.csv'
		with open(fname, 'r+') as f:
			# this reads in one line at a time from stdin
			date_previous = None 
			ticker_previous = None

			observation = {}
			observationPrevious = {}
			isFirstObservation = True

			lineo = 0

			for i, line in enumerate(f):
				#print line
				fList = line.split(",")
				date = fList[0]
				value = float(fList[1])
				ticker = str(fList[2])
				fundamental = str(fList[3])
				lineo += 1
				if (lineo == 10000):
					break

				if (date_previous == None):
					date_previous = date
				elif (date_previous != date):
					if (not isFirstObservation):
						#break
						observedData = gradientParser.getObservation(observationPrevious, observation, selectedKeys)
						curState = state(observedData)
						action = agent.getAction(curState)
						priceChange = curState.getScore()
						reward = action * priceChange
						agent.update(reward, curState, action)
						fScoreRewards[hashVal] = agent.getTotalRewards()
						fScoreCorrect[hashVal] = agent.getPercentCorrect()
					else:
						isFirstObservation = False
					observationPrevious = copy.deepcopy(observation)
					observation = {}
					date_previous = date

				if (ticker_previous == None):
					ticker_previous = ticker
				elif (ticker_previous != ticker):
					isFirstObservation = True
					ticker_previous = ticker

				observation[fundamental] = value

		#outside read loop
		#print "FINISHED"
		print fScoreRewards[hashVal]
		print fScoreCorrect[hashVal]
		visited.append(hashVal)
		if (len(previousState.keys()) == 0 or util.flipCoin(gradientEpsilon) or fScoreRewards[previousState["hash"]] < fScoreRewards[hashVal]):
			previousState["hash"] = hashVal
			previousState["selected"] = selectedKeys
			previousState["remaining"] = remainingKeys
		elif (len(maxState.keys()) == 0 or fScoreRewards[hashVal] > maxState["score"]):
			maxState["hash"] = hashVal
			maxState["selected"] = selectedKeys
			maxState["remaining"] = remainingKeys
			maxState["score"] = fScoreRewards[hashVal]
			maxState["correct"] = fScoreCorrect[hashVal]

		repeatedState= True
		while (repeatedState):
			hashVal = previousState["hash"]
			selectedKeys = previousState["selected"]
			remainingKeys = previousState["remaining"]
			#either randomly remove a fundamental, or add one
			#don't want too few fundamentals, so only remove if there are more than 4
			#also don't want too many, so limit it at like 45
			if ((len(selectedKeys) > 4 and util.flipCoin(0.5)) or len(selectedKeys) > 45):
				randomKey = random.sample(selectedKeys, 1)[0]
				while (randomKey == '"PRICE"'):
					randomKey = random.sample(selectedKeys, 1)[0]
				selectedKeys.remove(randomKey)
				remainingKeys.append(randomKey)
			else:
				randomKey = random.sample(remainingKeys, 1)[0]
				selectedKeys.append(randomKey)
				remainingKeys.remove(randomKey)

			hashVal = hash(tuple(selectedKeys))
			if (hashVal not in visited):
				repeatedState = False
	print "FINAL SOLUTION"
	print maxState

run()



