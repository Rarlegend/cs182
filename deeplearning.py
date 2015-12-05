import json 
import csv
import collections
import sys
import copy
import dataParser
import numpy as np

xArray = []
yArray = []
numToRun = 10
numFactors = 55

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
		# for i in range(0, len(data)):
		# 	bucketRanges = buckets[i]
		# 	dataVal = data[i]
		# 	if (dataVal == None):
		# 		stateDef += [0]
		# 	else:
		# 		for j in range(1,len(bucketRanges)):
		# 			if (data[i] < bucketRanges[j]):
		# 				stateDef += [j]
		# 				break
		# self.stateDef = tuple(stateDef)
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

def run():
	initialized = False
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
		counter = 0

		for i, line in enumerate(f):
			#print line
			fList = line.split(",")
			date = fList[0]
			value = float(fList[1])
			ticker = str(fList[2])
			fundamental = str(fList[3])


			if (date_previous == None):
				date_previous = date
			elif (date_previous != date):
				if (not isFirstObservation):
					#break
					observedData = getObservation(observationPrevious, observation)
					curState = state(observedData)
					# action = agent.getAction(curState)
					priceChange = curState.getScore()
					# reward = action * priceChange
					# agent.update(reward, curState, action)
					oldPrice = observedData[1]
					newPrice = observedData[2]
					priceDiffPercent = 0
					if (oldPrice == None or newPrice == None or oldPrice <= 0 or newPrice <= 0):
						priceDiffPercent = 0
					else:
						priceDiffPercent = (float(newPrice) + float(oldPrice)) / float(oldPrice)
					createArray(observedData[0], priceDiffPercent)
					counter += 1
					#print observation
					#print observationPrevious

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

			if (value == None):
				value = 0
			observation[fundamental] = value

			if (counter == numToRun):
				print "asda"
				#print xArray
				#print yArray
				break
			#print observation
			#print observationPrevious

			# if lineo == 100000:
			# 	break

# parse through data
def getPercentChanges(start, end):
	percentChanges = []
	for i in range(len(start)):
		if (start[i] == None or end[i] == None or start[i] == float(0) or end[i] == float(0)):
			#percentChanges.append(None)
			percentChanges.append(0)
		else:
			diff = 0
			if (end[i] < 0 and start[i] < 0):
				start[i] = abs(start[i])
				end[i] = abs(end[i])
			elif (end[i] < 0):
				diff = 0
			elif (start[i] < 0):
				diff = 0
			else:
				diff = float(end[i] - start[i]) / float(start[i]) * 100
			if (diff < -100):
				print end[i]
				print start[i]
				sys.exit("WTF")
			percentChanges.append(diff)
	#print percentChanges
	return percentChanges

def getItems(sortedDict):
	items = []
	for i in sortedDict:
		items.append(i[1])
	
	return items


# return a single ticker/date combination with all parameters
def getObservation(data1, data2):
	#make sure to add a check to make sure both observations have all the data

	keys = ['"ACCOCI"', '"ASSETS"', '"ASSETSC"', '"ASSETSNC"', '"BVPS"', '"CAPEX"', '"CASHNEQ"', '"COR"', '"CURRENTRATIO"', '"DE"', '"DEBT"', '"DEPAMOR"', '"DILUTIONRATIO"', '"DPS"', '"EBIT"', '"EBITDA"', '"EBT"', '"EPS"', '"EPSDIL"', '"EQUITY"', '"FCF"', '"FCFPS"', '"GP"', '"INTANGIBLES"', '"INTEXP"', '"INVENTORY"', '"LIABILITIES"', '"LIABILITIESC"', '"LIABILITIESNC"', '"NCF"', '"NCFCOMMON"', '"NCFDEBT"', '"NCFDIV"', '"NCFF"', '"NCFI"', '"NCFO"', '"NCFX"', '"NETINC"', '"NETINCCMN"', '"NETINCDIS"', '"PAYABLES"', '"PB"', '"PREFDIVIS"', '"PRICE"', '"RECEIVABLES"', '"RETEARN"', '"REVENUE"', '"RND"', '"SGNA"', '"SHARESWA"', '"SHARESWADIL"', '"TANGIBLES"', '"TAXEXP"', '"TBVPS"', '"WORKINGCAPITAL"']
	#keys = ['"PRICE"']

	# Price removed
	#keys = ['"ACCOCI"', '"ASSETS"', '"ASSETSC"', '"ASSETSNC"', '"BVPS"', '"CAPEX"', '"CASHNEQ"', '"COR"', '"CURRENTRATIO"', '"DE"', '"DEBT"', '"DEPAMOR"', '"DILUTIONRATIO"', '"DPS"', '"EBIT"', '"EBITDA"', '"EBT"', '"EPS"', '"EPSDIL"', '"EQUITY"', '"FCF"', '"FCFPS"', '"GP"', '"INTANGIBLES"', '"INTEXP"', '"INVENTORY"', '"LIABILITIES"', '"LIABILITIESC"', '"LIABILITIESNC"', '"NCF"', '"NCFCOMMON"', '"NCFDEBT"', '"NCFDIV"', '"NCFF"', '"NCFI"', '"NCFO"', '"NCFX"', '"NETINC"', '"NETINCCMN"', '"NETINCDIS"', '"PAYABLES"', '"PB"', '"PREFDIVIS"', '"RECEIVABLES"', '"RETEARN"', '"REVENUE"', '"RND"', '"SGNA"', '"SHARESWA"', '"SHARESWADIL"', '"TANGIBLES"', '"TAXEXP"', '"TBVPS"', '"WORKINGCAPITAL"']

	# data1 = collections.OrderedDict(sorted(data1.items()))
	# data2 = collections.OrderedDict(sorted(data2.items()))

	data1Complete = {}
	data2Complete = {}

	for key in keys:
		try:
			data1[key]
			data1Complete[key] = data1[key]
		except:
			data1Complete[key] = None

		try:
			data2[key]
			data2Complete[key] = data2[key]
		except:
			data2Complete[key] = None

	data1Complete_sorted = collections.OrderedDict(sorted(data1Complete.items()))
	data2Complete_sorted = collections.OrderedDict(sorted(data2Complete.items()))

	data = getItems(data1Complete_sorted.items());
	nextData = getItems(data2Complete_sorted.items());

	percentChanges = getPercentChanges(data,nextData)
	
	curPrice = data1Complete['"PRICE"']
	nextPrice = data2Complete['"PRICE"']
	
	#print "DATA"
	# print data1
	# print data2
	#print percentChanges
	return [percentChanges, curPrice, nextPrice]

def createArray(observedData, priceChange):
	#print observedData
	xArray.append(observedData)
	yArray.append(priceChange)


def deeplearning ():

	X = np.array(xArray)
	Y = np.array([yArray])

	def nonlin(x,deriv=False):
		if(deriv==True):
			return x*(1-x)

		return 1/(1+np.exp(-x))
		
	# X = np.array([[0,0,1],
	# 			[0,1,1],
	# 			[1,0,1],
	# 			[1,1,1]])
					
	# y = np.array([[0],
	# 			[1],
	# 			[1],
	# 			[0]])

	np.random.seed(1)

	# randomly initialize our weights with mean 0
	syn0 = 2*np.random.random((numFactors,numToRun)) - 1
	syn1 = 2*np.random.random((numToRun,1)) - 1

	for j in xrange(60000):
		# Feed forward through layers 0, 1, and 2
		#print X
		#l0 is 10 by 55
		l0 = X
		#l1 is 10 by 10
		l1 = nonlin(np.dot(l0,syn0))
		#l2 is 1 by 10
		l2 = nonlin(np.dot(l1,syn1))
		

		# how much did we miss the target value?
		l2_error = Y.T - l2
		
		if (j% 10000) == 0:
			# print l0
			# print Y
			# print syn0
			print "Error:" + str(np.mean(np.abs(l2_error)))
			
		# in what direction is the target value?
		# were we really sure? if so, don't change too much.
		l2_delta = l2_error*nonlin(l2,deriv=True)

		# how much did each l1 value contribute to the l2 error (according to the weights)?
		# print l2_error
		# print l2_delta
		# print syn1.T
		# print syn0
		# print l0
		# print l1
		l1_error = l2_delta.dot(syn1.T)
		
		# in what direction is the target l1?
		# were we really sure? if so, don't change too much.
		l1_delta = l1_error * nonlin(l1,deriv=True)

		syn1 += l1.T.dot(l2_delta)
		syn0 += l0.T.dot(l1_delta)
		# break


run()
deeplearning()
