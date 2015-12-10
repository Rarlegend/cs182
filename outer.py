import myownq
import random
import util
import math
import geneticAlgorithm

#list of all fundamentals used including price
allKeys = ['"ACCOCI"', '"ASSETS"', '"ASSETSC"', '"ASSETSNC"', '"BVPS"', '"CAPEX"', '"CASHNEQ"', '"COR"', '"CURRENTRATIO"', '"DE"', '"DEBT"', '"DEPAMOR"', '"DILUTIONRATIO"', '"DPS"', '"EBIT"', '"EBITDA"', '"EBT"', '"EPS"', '"EPSDIL"', '"EQUITY"', '"FCF"', '"FCFPS"', '"GP"', '"INTANGIBLES"', '"INTEXP"', '"INVENTORY"', '"LIABILITIES"', '"LIABILITIESC"', '"LIABILITIESNC"', '"NCF"', '"NCFCOMMON"', '"NCFDEBT"', '"NCFDIV"', '"NCFF"', '"NCFI"', '"NCFO"', '"NCFX"', '"NETINC"', '"NETINCCMN"', '"NETINCDIS"', '"PAYABLES"', '"PB"', '"PREFDIVIS"', '"RECEIVABLES"', '"RETEARN"', '"REVENUE"', '"RND"', '"SGNA"', '"SHARESWA"', '"SHARESWADIL"', '"TANGIBLES"', '"TAXEXP"', '"TBVPS"', '"WORKINGCAPITAL"']
#list with price removed
keys = ['"ACCOCI"', '"ASSETS"', '"ASSETSC"', '"ASSETSNC"', '"BVPS"', '"CAPEX"', '"CASHNEQ"', '"COR"', '"CURRENTRATIO"', '"DE"', '"DEBT"', '"DEPAMOR"', '"DILUTIONRATIO"', '"DPS"', '"EBIT"', '"EBITDA"', '"EBT"', '"EPS"', '"EPSDIL"', '"EQUITY"', '"FCF"', '"FCFPS"', '"GP"', '"INTANGIBLES"', '"INTEXP"', '"INVENTORY"', '"LIABILITIES"', '"LIABILITIESC"', '"LIABILITIESNC"', '"NCF"', '"NCFCOMMON"', '"NCFDEBT"', '"NCFDIV"', '"NCFF"', '"NCFI"', '"NCFO"', '"NCFX"', '"NETINC"', '"NETINCCMN"', '"NETINCDIS"', '"PAYABLES"', '"PB"', '"PREFDIVIS"', '"RECEIVABLES"', '"RETEARN"', '"REVENUE"', '"RND"', '"SGNA"', '"SHARESWA"', '"SHARESWADIL"', '"TANGIBLES"', '"TAXEXP"', '"TBVPS"', '"WORKINGCAPITAL"']
gradientEpsilon = 0.01
popN = 25 # n number of chromos per population
genesPerCh = 54
max_iterations = 5000
chromos = geneticAlgorithm.generatePop(popN) #generate new population of random chromosomes
iterations = 0

#stochastic descent with random restarts
def runStochasticDescent():
	initialized = False
	#randomly select 10 fundamentals to use
	selectedKeys = random.sample(keys, 10)
	#add in price
	selectedKeys += ['"PRICE"']
	remainingKeys = [key for key in keys if key not in selectedKeys]
	hashVal = hash(tuple(selectedKeys))
	#store the scores for this set of fundamentals
	fScoreCorrect = dict()
	fScoreRewards = dict()
	previousState = dict()
	visited = []
	maxState = dict()

	#loop through 100,000 iterations
	for x in range(1,100000):
		#random restarts
		if (x%10000 == 0):
			selectedKeys = random.sample(keys, 10)
			selectedKeys += ['"PRICE"']
			remainingKeys = [key for key in keys if key not in selectedKeys]
			hashVal = hash(tuple(selectedKeys))
			previousState = dict()
			#print ("RESTART")

		#get the score for this set of fundamentals by running the inner loop
		result = myownq.runInnerLoop(selectedKeys)
		fScoreRewards[hashVal] = result[0]
		fScoreCorrect[hashVal] = result[1]
		#save the inner loop agent that ran the inner q-learning for this set
		agent = result[2]
		visited.append(hashVal)
		move = False
		#move if its the first step
		if (len(previousState.keys()) == 0):
			move = True
		#move if the new state has a better score
		elif (fScoreRewards[previousState["hash"]] < fScoreRewards[hashVal]):
			move = True
		#move randomly with a chance equal to gradientEpsilon
		else:
			move = util.flipCoin(gradientEpsilon)
		if (move):
			#update values for previous state
			previousState["hash"] = hashVal
			previousState["selected"] = selectedKeys
			previousState["remaining"] = remainingKeys
			#print (fScoreRewards[hashVal])
			#print (fScoreCorrect[hashVal])

			#update max state if necessary
			if (len(maxState.keys()) == 0 or fScoreRewards[hashVal] > maxState["score"]):
				maxState["hash"] = hashVal
				maxState["selected"] = selectedKeys
				maxState["remaining"] = remainingKeys
				maxState["score"] = fScoreRewards[hashVal]
				maxState["correct"] = fScoreCorrect[hashVal]
				maxState["agent"] = agent

		#avoid repeated states
		repeatedState = True
		numRepeatedStates = 0
		while (repeatedState):
			numRepeatedStates += 1
			hashVal = previousState["hash"]
			selectedKeys = previousState["selected"]
			remainingKeys = previousState["remaining"]
			#either randomly remove a fundamental, or add one
			#don't want too few fundamentals, so only remove if there are more than 4
			#also don't want too many, so limit it at around 45
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
			#we are probably stuck in an infinite loop if this occurs, so we need to randomly sample
			if (numRepeatedStates >=1000):
				selectedKeys = random.sample(keys, 10)
				selectedKeys += ['"PRICE"']
				remainingKeys = [key for key in keys if key not in selectedKeys]
				hashVal = hash(tuple(selectedKeys))
				previousState = dict()

	#print ("FINAL SOLUTION")
	print (maxState)

#random anneal probablity, dependent on time
def annealSchedule(delta, time):
	return math.exp(float(delta) / float(100001 - time)**0.4)

#save the agent returned from the max state
simulatedAgent = myownq.qAgent()

#Simulated Annealing
def runSimulatedAnnealing():
	initialized = False
	#no price in these keys
	selectedKeys = random.sample(keys, 10)
	selectedKeys += ['"PRICE"']
	remainingKeys = [key for key in keys if key not in selectedKeys]
	hashVal = hash(tuple(selectedKeys))
	fScoreCorrect = dict()
	fScoreRewards = dict()
	previousState = dict()
	visited = []
	maxState = dict()
	maxAgent = None
	testing = False

	#run the iterations
	for x in range(1,100000):
		# if (x % 100 == 0):
		# 	print x
		# if (x < 10):
		result = myownq.runInnerLoop(selectedKeys, myownq.qAgent())
		# else:
		# 	if (not testing):
		# 		#print maxState
		# 		testing = True
		# 	maxAgent = maxState["agent"]
		# 	selectedKeys = maxState["selected"]
		# 	result = myownq.runTestLoop(selectedKeys, maxAgent)
		# 	#print "RESULT"
		# 	#print result
		# 	#print maxState

		fScoreRewards[hashVal] = result[0]
		fScoreCorrect[hashVal] = result[1]
		agent = result[2]
		visited.append(hashVal)

		move = False
		#move if we are on the first step
		if (len(previousState.keys()) == 0):
			move = True
		else:
			delta = fScoreRewards[hashVal] - fScoreRewards[previousState["hash"]]
			#move if we move to a better state
			if (delta >= 0):
				move = True
			#move with a probablity defined by the anneal schedule function
			else:
				move = random.random() <= annealSchedule(delta, x)

		if (len(previousState.keys()) == 0 or move):
			previousState["hash"] = hashVal
			previousState["selected"] = selectedKeys
			previousState["remaining"] = remainingKeys
			# print (fScoreRewards[hashVal])
			# print (fScoreCorrect[hashVal])
			# print x
			if (len(maxState.keys()) == 0 or fScoreRewards[hashVal] > maxState["score"]):
				maxState["hash"] = hashVal
				maxState["selected"] = selectedKeys
				maxState["remaining"] = remainingKeys
				maxState["score"] = fScoreRewards[hashVal]
				maxState["correct"] = fScoreCorrect[hashVal]
				maxState["agent"] = agent

		repeatedState= True
		numRepeatedStates = 0
		#avoid repeating states
		while (repeatedState):
			numRepeatedStates += 1
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
			if (numRepeatedStates >=1000):
				selectedKeys = random.sample(keys, 10)
				selectedKeys += ['"PRICE"']
				remainingKeys = [key for key in keys if key not in selectedKeys]

	# print ("FINAL SOLUTION")
	print (maxState)
	# agent = maxState["agent"]
	# agent.setTestingOn()
	#print maxAgent.getTotalRewards()
	#print maxAgent.getPercentCorrect()

#run the genetic algorithm
def runGeneticAlgorithm():
	

  	while True:
  		if (iterations == max_iterations):
  			#get the new generation, ranked by fitness score
	 		rankedPop = geneticAlgorithm.rankPop(chromos) 
	 		#print(len(rankedPop))
	 		#print rankedPop
	  		chromos = []
	  		#get the best agent from the population
	  		agent = geneticAlgorithm.iteratePop(rankedPop, popN, True)
	  		listKeys = agent[0]
	  		keyNames = []
	  		#find the best keys for this agent
	  		for i in range(len(listKeys)):
	  			if (listKeys[i] == 1):
	  				keyNames.append(allKeys[i])
	  		print agent
	  		print keyNames
	  		break
		# take the population of random chromos and rank them based on their fitness score/proximity to target output
		rankedPop = geneticAlgorithm.rankPop(chromos) 
		#print rankedPop

  		chromos = []
  		#get the new chromosomes
  		chromos = geneticAlgorithm.iteratePop(rankedPop, popN, False)
		
  		iterations += 1


#runStochasticDescent()
runSimulatedAnnealing()
#runGeneticAlgorithm()


