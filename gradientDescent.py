import myownq
import random
import util
import math
import geneticAlgorithm






#stochastic descent with random restarts
def runStochasticDescent():
	gradientEpsilon = 0.01
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
			print ("RESTART")

		result = myownq.runInnerLoop(selectedKeys)
		fScoreRewards[hashVal] = result[0]
		fScoreCorrect[hashVal] = result[1]
		agent = result[2]
		visited.append(hashVal)
		move = False
		if (len(previousState.keys()) == 0):
			move = True
		elif (fScoreRewards[previousState["hash"]] < fScoreRewards[hashVal]):
			move = True
		else:
			move = util.flipCoin(gradientEpsilon)
		if (move):
			previousState["hash"] = hashVal
			previousState["selected"] = selectedKeys
			previousState["remaining"] = remainingKeys
			print (fScoreRewards[hashVal])
			print (fScoreCorrect[hashVal])
			if (len(maxState.keys()) == 0 or fScoreRewards[hashVal] > maxState["score"]):
				maxState["hash"] = hashVal
				maxState["selected"] = selectedKeys
				maxState["remaining"] = remainingKeys
				maxState["score"] = fScoreRewards[hashVal]
				maxState["correct"] = fScoreCorrect[hashVal]
				maxState["agent"] = agent

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
	print ("FINAL SOLUTION")
	print (maxState)

def annealSchedule(delta, time):
	return math.exp(float(delta) / float(100001 - time)**0.4)

simulatedAgent = myownq.qAgent()

#The function that runs the inner Q-learning
def runSimulatedAnnealing():
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

	for x in range(1,10000):

		result = myownq.runInnerLoop(selectedKeys)
		fScoreRewards[hashVal] = result[0]
		fScoreCorrect[hashVal] = result[1]
		agent = result[2]
		visited.append(hashVal)

		move = False
		if (len(previousState.keys()) == 0):
			move = True
		else:
			delta = fScoreRewards[hashVal] - fScoreRewards[previousState["hash"]]
			if (delta >= 0):
				move = True
			else:
				move = random.random() <= annealSchedule(delta, x)

		if (len(previousState.keys()) == 0 or move):
			previousState["hash"] = hashVal
			previousState["selected"] = selectedKeys
			previousState["remaining"] = remainingKeys
			print (fScoreRewards[hashVal])
			print (fScoreCorrect[hashVal])
			if (len(maxState.keys()) == 0 or fScoreRewards[hashVal] > maxState["score"]):
				maxState["hash"] = hashVal
				maxState["selected"] = selectedKeys
				maxState["remaining"] = remainingKeys
				maxState["score"] = fScoreRewards[hashVal]
				maxState["correct"] = fScoreCorrect[hashVal]
				maxState["agent"] = agent

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
	print ("FINAL SOLUTION")
	print (maxState)

def runGeneticAlgorithm():
	popN = 10 # n number of chromos per population
	genesPerCh = 54
	max_iterations = 1000
  	chromos = geneticAlgorithm.generatePop(popN) #generate new population of random chromosomes
  	iterations = 0

  	while iterations != max_iterations:
  		if (iterations == 1000):
	 		rankedPop = geneticAlgorithm.rankPop(chromos) 
	 		print rankedPop
	  		chromos = []
	  		agent = geneticAlgorithm.iteratePop(rankedPop, popN, True)
	  		break
		# take the pop of random chromos and rank them based on their fitness score/proximity to target output
		rankedPop = geneticAlgorithm.rankPop(chromos) 
		#print rankedPop

  		chromos = []
  		chromos = geneticAlgorithm.iteratePop(rankedPop, popN, False)
		
  		iterations += 1


#runStochasticDescent()
#runSimulatedAnnealing()
runGeneticAlgorithm()


