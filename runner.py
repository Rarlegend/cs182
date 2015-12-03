import actualQ
import dataParser

#bucket ranges for different metrics
buckets = dict()
buckets[0] = [(0,10),(10,20),(20,30),(30,100),(100,1000)]
buckets[1] = [(0,10),(10,20),(20,30),(30,100),(100,1000)]
buckets[2] = [(0,10),(10,20),(20,30),(30,100),(100,1000)]
buckets[3] = [(0,10),(10,20),(20,30),(30,100),(100,1000)]
buckets[4] = [(0,10),(10,20),(20,30),(30,100),(100,1000)]

#take data and put it into buckets defined somewhere else
class state():
	def __init__(self, values):
		data = values[0]
		newPrice = values[2]
		self.data = data
		self.curPrice = values[1]
		self.newPrice = newPrice
		stateDef = []
		#place values into buckets
		for i in range(1, len(data)):
			bucketRanges = buckets[i]
			dataVal = data[i]
			for j in range(len(bucketRanges)):
				if (i < bucketRanges[j][1]):
					stateDef += [j]
		self.stateDef = tuple(stateDef)
	def getScore(self):
		priceChange = self.newPrice - self.curPrice
		return priceChange
	#-1 = predict lower price, 1 = predict higher price
	def getLegalActions(self):
		return [-1,1]


agent = actualQ.innerQAgent()
#The function that runs the inner Q-learning
def run():
	#loop through some subset of the dataset
	observation = dataParser.getObservation()
	initialState = state(observation)
	agent.registerInitialState(initialState)
	keepRunning = True
	while (keepRunning):
		observation = dataParser.getObservation()
		curState = state(observation)
		agent.observationFunction(curState)
		keepRunning = False

	observation = dataParser.getObservation()
	finalState = state(observation)
	agent.final(finalState)

run()



