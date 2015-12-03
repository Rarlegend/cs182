import json 
import csv
import collections

# parse through data
def getPercentChanges(start, end):
	percentChanges = []
	for i in range(len(start)):
		if (start[i] == None or end[i] == None or start[i] == float(0) or end[i] == float(0)):
			percentChanges.append(None)
		else:
			diff = float(end[i] - start[i]) / float(start[i]) * 100
			percentChanges.append(diff)
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
	
	return [percentChanges, curPrice, nextPrice]

# open data row by row to avoid memory overflow
fname = 'data_cleaned.csv'
with open(fname, 'r+') as f:
	# this reads in one line at a time from stdin
	date_previous = None 
	ticker_previous = None

	observation = {}
	observationPrevious = {}

	lineo = 0

	for i, line in enumerate(f):
		#print i
		#print line
		fList = line.split(",")
		date = fList[0]
		value = float(fList[1])
		ticker = str(fList[2])
		fundamental = str(fList[3])

		if lineo == 100000:
			break

		if ticker_previous == None:
			ticker_previous = ticker
			date_previous = date

		if date == date_previous:
			observation[fundamental] = value

		if date != date_previous:
			lineo += 1
			#print observation
			getObservation(observation, observationPrevious)

			observationPrevious = observation
			observation = {}
			observation[fundamental] = value

			date_previous = date
