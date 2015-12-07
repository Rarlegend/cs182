import random
import myownq
import operator

keys = ['"ACCOCI"', '"ASSETS"', '"ASSETSC"', '"ASSETSNC"', '"BVPS"', '"CAPEX"', '"CASHNEQ"', '"COR"', '"CURRENTRATIO"', '"DE"', '"DEBT"', '"DEPAMOR"', '"DILUTIONRATIO"', '"DPS"', '"EBIT"', '"EBITDA"', '"EBT"', '"EPS"', '"EPSDIL"', '"EQUITY"', '"FCF"', '"FCFPS"', '"GP"', '"INTANGIBLES"', '"INTEXP"', '"INVENTORY"', '"LIABILITIES"', '"LIABILITIESC"', '"LIABILITIESNC"', '"NCF"', '"NCFCOMMON"', '"NCFDEBT"', '"NCFDIV"', '"NCFF"', '"NCFI"', '"NCFO"', '"NCFX"', '"NETINC"', '"NETINCCMN"', '"NETINCDIS"', '"PAYABLES"', '"PB"', '"PREFDIVIS"', '"RECEIVABLES"', '"RETEARN"', '"REVENUE"', '"RND"', '"SGNA"', '"SHARESWA"', '"SHARESWADIL"', '"TANGIBLES"', '"TAXEXP"', '"TBVPS"', '"WORKINGCAPITAL"']
crossover_rate = 0.7
mutation_rate = 0.05

"""Generates random population of chromos"""
def generatePop (popN):
	chromos = []
	listFundamentals = []
	for x in range(54):
		listFundamentals.append(x)
	for eachChromo in range(popN):
		chromo = [0]*54
		numFundamentals = random.randint(1,54)
		selected = random.sample(listFundamentals, numFundamentals)
		for i in range(len(listFundamentals)):
			if (i in selected):
				chromo[i] = 1
		chromos.append(chromo)
		#print chromos
	return chromos

"""Calulates fitness as a fraction of the total fitness"""
def calcFitness (errors):
	fitnessScores = []
	totalError = sum(errors)
	if (totalError <= 0):
		totalError = 1
	i = 0
	# fitness scores are a fraction of the total error
	for error in errors:
		fitnessScores.append (float(errors[i])/float(totalError))
		i += 1
	return fitnessScores

"""Takes a population of chromosomes and returns a list of tuples where each chromo is paired to its fitness scores and ranked accroding to its fitness"""
def rankPop (chromos):
	errors, results = [], []
	#print chromos
	for chromo in chromos: 
		selectedKeys = []
		for i in range(len(chromo)):
			if (chromo[i] == 1):
				selectedKeys.append(keys[i])
		selectedKeys.append('"PRICE"')
		scores = myownq.runInnerLoop(selectedKeys)
		if (scores[0] <= 0):
			errors.append(1)
		else:
			errors.append(scores[0])
		results.append(scores)
		#print scores
	#print errors

	fitnessScores = calcFitness (errors) # calc fitness scores from the erros calculated
	pairedPop = zip ( chromos, errors, results, fitnessScores) # pair each chromo with its protein, ouput and fitness score
	rankedPop = sorted ( pairedPop,key = operator.itemgetter(-1), reverse = True ) # sort the paired pop by ascending fitness score
	return rankedPop

""" taking a ranked population selects two of the fittest members using roulette method"""
def selectFittest (fitnessScores, rankedChromos):
	while (1 == 1): # ensure that the chromosomes selected for breeding are have different indexes in the population
		index1 = roulette (fitnessScores)
		index2 = roulette (fitnessScores)
		if index1 == index2:
			continue
		else:
			break

	ch1 = rankedChromos[index1] # select  and return chromosomes for breeding 
	ch2 = rankedChromos[index2]
	return ch1, ch2

"""Fitness scores are fractions, their sum = 1. Fitter chromosomes have a larger fraction.  """
def roulette (fitnessScores):
	index = 0
	cumalativeFitness = 0.0
	r = random.random()
  
	for i in range(len(fitnessScores)): # for each chromosome's fitness score
		cumalativeFitness += fitnessScores[i] # add each chromosome's fitness score to cumalative fitness

		if cumalativeFitness > r: # in the event of cumalative fitness becoming greater than r, return index of that chromo
			return i

def crossover (ch1, ch2):
  	# at a random chiasma
  	r = random.randint(0,54)
  	return ch1[:r]+ch2[r:], ch2[:r]+ch1[r:]


def mutate (ch):
  	mutatedCh = []
	for i in ch:
		if random.random() < mutation_rate:
		  	if i == 1:
				mutatedCh.append(0)
		  	else:
				mutatedCh.append(1)
		else:
		  	mutatedCh.append(i)
	#assert mutatedCh != ch
  	return mutatedCh

"""Using breed and mutate it generates two new chromos from the selected pair"""
def breed (ch1, ch2):
  
	newCh1, newCh2 = [], []
	if random.random() < crossover_rate: # rate dependent crossover of selected chromosomes
		newCh1, newCh2 = crossover(ch1, ch2)
	else:
		newCh1, newCh2 = ch1, ch2
	newnewCh1 = mutate (newCh1) # mutate crossovered chromos
	newnewCh2 = mutate (newCh2)
  
	return newnewCh1, newnewCh2

""" Taking a ranked population return a new population by breeding the ranked one"""
def iteratePop (rankedPop, popN, getBestAgent):
	fitnessScores = [ item[-1] for item in rankedPop ] # extract fitness scores from ranked population
	rankedChromos = [ item[0] for item in rankedPop ] # extract chromosomes from ranked population
	scores = [ item[1] for item in rankedPop ]
	if (getBestAgent):
		maxIndex = scores.index(max(scores))
		return rankedPop[maxIndex][2][-1]
	else:
		newpop = []
		numElites = popN/8
		if (numElites < 1):
			numElites = 1
		newpop.extend(rankedChromos[:numElites]) # known as elitism, conserve the best solutions to new population

		while len(newpop) < popN:
			ch1, ch2 = [], []
			ch1, ch2 = selectFittest (fitnessScores, rankedChromos) # select two of the fittest chromos
			
			ch1, ch2 = breed (ch1, ch2) # breed them to create two new chromosomes 
			newpop.append(ch1) # and append to new population
			newpop.append(ch2)
		return newpop

