import myownq
import dataParser

#bucket ranges for different metrics
buckets = dict()
for i in range(55):
	#buckets[i] = [0,-50,-40,-30,-20,-10,10,20,30,40,50,10000000]
	#buckets[i] = [0,10000000]
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
			#print line
			fList = line.split(",")
			date = fList[0]
			value = float(fList[1])
			ticker = str(fList[2])
			fundamental = str(fList[3])

			# if lineo == 100000:
			# 	break

			if ticker_previous == None:
				ticker_previous = ticker
				date_previous = date

			if date == date_previous:
				observation[fundamental] = value

			if date != date_previous:
				lineo += 1
				#print observation
				observedData = dataParser.getObservation(observation, observationPrevious)

				observationPrevious = observation
				observation = {}
				observation[fundamental] = value

				date_previous = date

				curState = state(observedData)
				action = agent.getAction(curState)
				priceChange = curState.getScore()
				reward = action * priceChange
				agent.update(reward, curState, action)
				print agent.getPercentCorrect()
				print agent.getTotalRewards()

				if (i%200000 == 0):
					agent.finish()


run()



