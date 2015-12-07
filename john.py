import json 
import csv
import collections
import sys
import random, util, time
import copy
import gradientParser

totalSum = 0
totalPlus = 0
totalMinus = 0
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
							

							change = observation['"PRICENEXT"'] - observation['"PRICE"']
							totalSum += change
							if (observation['"PRICENEXT"'] > observation['"PRICE"']):
								totalPlus += change
							else:
								totalMinus += change
					else:
						isFirstObservation = False
					observationPrevious = copy.deepcopy(observation)
					observation = {}
					date_previous = date

			observation[fundamental] = value
print totalSum
print totalPlus
print totalMinus
print totalPlus - totalMinus