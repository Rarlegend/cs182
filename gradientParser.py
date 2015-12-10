import json 
import csv
import collections
import sys

# parse through data to get percent changes between two observations
def getPercentChanges(start, end):
	percentChanges = []
	for i in range(len(start)):
		if (start[i] == None or end[i] == None or start[i] == float(0) or end[i] == float(0)):
			percentChanges.append(None)
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
def getObservation(data1, data2, keys):
	#make sure to add a check to make sure both observations have all the data
	allKeys = ['"ACCOCI"', '"ASSETS"', '"ASSETSC"', '"ASSETSNC"', '"BVPS"', '"CAPEX"', '"CASHNEQ"', '"COR"', '"CURRENTRATIO"', '"DE"', '"DEBT"', '"DEPAMOR"', '"DILUTIONRATIO"', '"DPS"', '"EBIT"', '"EBITDA"', '"EBT"', '"EPS"', '"EPSDIL"', '"EQUITY"', '"FCF"', '"FCFPS"', '"GP"', '"INTANGIBLES"', '"INTEXP"', '"INVENTORY"', '"LIABILITIES"', '"LIABILITIESC"', '"LIABILITIESNC"', '"NCF"', '"NCFCOMMON"', '"NCFDEBT"', '"NCFDIV"', '"NCFF"', '"NCFI"', '"NCFO"', '"NCFX"', '"NETINC"', '"NETINCCMN"', '"NETINCDIS"', '"PAYABLES"', '"PB"', '"PREFDIVIS"', '"PRICE"', '"RECEIVABLES"', '"RETEARN"', '"REVENUE"', '"RND"', '"SGNA"', '"SHARESWA"', '"SHARESWADIL"', '"TANGIBLES"', '"TAXEXP"', '"TBVPS"', '"WORKINGCAPITAL"']
	#keys = ['"PRICE"']

	# Price removed
	#keys = ['"ACCOCI"', '"ASSETS"', '"ASSETSC"', '"ASSETSNC"', '"BVPS"', '"CAPEX"', '"CASHNEQ"', '"COR"', '"CURRENTRATIO"', '"DE"', '"DEBT"', '"DEPAMOR"', '"DILUTIONRATIO"', '"DPS"', '"EBIT"', '"EBITDA"', '"EBT"', '"EPS"', '"EPSDIL"', '"EQUITY"', '"FCF"', '"FCFPS"', '"GP"', '"INTANGIBLES"', '"INTEXP"', '"INVENTORY"', '"LIABILITIES"', '"LIABILITIESC"', '"LIABILITIESNC"', '"NCF"', '"NCFCOMMON"', '"NCFDEBT"', '"NCFDIV"', '"NCFF"', '"NCFI"', '"NCFO"', '"NCFX"', '"NETINC"', '"NETINCCMN"', '"NETINCDIS"', '"PAYABLES"', '"PB"', '"PREFDIVIS"', '"RECEIVABLES"', '"RETEARN"', '"REVENUE"', '"RND"', '"SGNA"', '"SHARESWA"', '"SHARESWADIL"', '"TANGIBLES"', '"TAXEXP"', '"TBVPS"', '"WORKINGCAPITAL"']

	# data1 = collections.OrderedDict(sorted(data1.items()))
	# data2 = collections.OrderedDict(sorted(data2.items()))

	data1Complete = {}
	data2Complete = {}

	for key in allKeys:
		if (key not in keys):
			data1Complete[key] = None
			data2Complete[key] = None
		else:
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
	curPrice = data2['"PRICE"']
	nextPrice = data2['"PRICENEXT"']
	
	# print "DATA"
	# print data1
	# print data2
	return [percentChanges, curPrice, nextPrice]
