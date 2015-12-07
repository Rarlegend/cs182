from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_boston
from pprint import pprint
import myownq
import random
import util
import math
  
xData = []
yData = []

selectedKeys = ['"ACCOCI"', '"ASSETS"', '"ASSETSC"', '"ASSETSNC"', '"BVPS"', '"CAPEX"', '"CASHNEQ"', '"COR"', '"CURRENTRATIO"', '"DE"', '"DEBT"', '"DEPAMOR"', '"DILUTIONRATIO"', '"DPS"', '"EBIT"', '"EBITDA"', '"EBT"', '"EPS"', '"EPSDIL"', '"EQUITY"', '"FCF"', '"FCFPS"', '"GP"', '"INTANGIBLES"', '"INTEXP"', '"INVENTORY"', '"LIABILITIES"', '"LIABILITIESC"', '"LIABILITIESNC"', '"NCF"', '"NCFCOMMON"', '"NCFDEBT"', '"NCFDIV"', '"NCFF"', '"NCFI"', '"NCFO"', '"NCFX"', '"NETINC"', '"NETINCCMN"', '"NETINCDIS"', '"PAYABLES"', '"PB"', '"PREFDIVIS"', '"PRICE"', '"RECEIVABLES"', '"RETEARN"', '"REVENUE"', '"RND"', '"SGNA"', '"SHARESWA"', '"SHARESWADIL"', '"TANGIBLES"', '"TAXEXP"', '"TBVPS"', '"WORKINGCAPITAL"']

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
					priceChange = curState.getScore()
					xData.append(observedData[0])
					yData.append(priceChange)
			else:
				isFirstObservation = False
			observationPrevious = copy.deepcopy(observation)
			observation = {}
			date_previous = date

	observation[fundamental] = value

X = scaler.fit_transform(xData)
Y = yData
names = selectedKeys
  
lasso = Lasso(alpha=.3)
lasso.fit(X, Y)

print lasso.coef_
print names
