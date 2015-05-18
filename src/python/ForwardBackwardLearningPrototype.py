# own learning algorithm
# "forward backward learning"

# only forward reasoning is implemented
# TODO
# * backward (from result to chosen varible)
# * repetition (interpreter)


import math


def abs2(value):
	if value > 0.0:
		return value
	else:
		return -value


class Operation(object):
	def __init__(self):
		pass

	def reverseForInputA(self, valueB, targetResultValue):
		pass

	def forward(self, a, b):
		pass

class AddOperation(Operation):
	def reverseForInputA(self, valueB, targetResultValue):
		return targetResultValue - valueB

	def forward(self, a, b):
		return a + b

class MulOperation(Operation):
	def reverseForInputA(self, valueB, targetResultValue):
		return targetResultValue / valueB

	def forward(self, a, b):
		return a * b




class Data(object):
	def __init__(self, operation):
		self.operation = operation
		self.valueB = None

		self.tempValueA = None # input value

		self.tempResult = None





class DagElement(object):
	def __init__(self, data):
		self.childIndices = []
		self.data = data

class Dag(object):
	def __init__(self):
		self.elements = []




class IRate(object):
	def __init__(self):
		pass

	# returns zero if value is perfect
	def rate(self, dag):
		pass

class TestRate(IRate):
	def __init__(self, targetValue):
		self.targetValue = targetValue

	def rate(self, dag):
		return abs2(dag.elements[1].data.tempResult - self.targetValue)



class ForwardBackwardLearning(object):
	def __init__(self):
		self.dag = Dag()
		self.rateObject = None

	def calculateDagForward(self):
		for iterationDagElement in self.dag.elements:
			iterationDagElement.data.tempResult = iterationDagElement.data.operation.forward(iterationDagElement.data.tempValueA, iterationDagElement.data.valueB)

			for currentChildIndex in iterationDagElement.childIndices:
				self.dag.elements[currentChildIndex].data.tempValueA = iterationDagElement.data.tempResult

	def rate(self, dag):
		return self.rateObject.rate(dag)

	def iteration(self):
		self.calculateDagForward()
		currentRating = self.rate(self.dag)

		ratingAfterVariableChanges = []

		for i in range(len(self.dag.elements)):
			self.dag.elements[i].data.valueB += 0.01
			self.calculateDagForward()
			ratingAfterChange = self.rate(self.dag)
			ratingAfterVariableChanges.append(ratingAfterChange)

			self.dag.elements[i].data.valueB -= 0.01 # reverse change

			self.dag.elements[i].data.valueB -= 0.01
			self.calculateDagForward()
			ratingAfterChange = self.rate(self.dag)
			ratingAfterVariableChanges.append(ratingAfterChange)

			self.dag.elements[i].data.valueB += 0.01 # reverse change
		
		# get minimal index of change

		minIndex = 0
		minValue = ratingAfterVariableChanges[0]

		for i in range(len(ratingAfterVariableChanges)):
			iterationRating = ratingAfterVariableChanges[i]

			if iterationRating < minValue:
				minValue = iterationRating
				minIndex = i

		# apply change which minimizes error

		if (minIndex % 2) == 0 :
			self.dag.elements[minIndex/2].data.valueB += 0.01
		else:
			self.dag.elements[minIndex/2].data.valueB -= 0.01

addDagElement = DagElement(Data(AddOperation()))
addDagElement.childIndices = [1]
addDagElement.data.tempValueA = 6
addDagElement.data.valueB = 5.1

mulDagElement = DagElement(Data(AddOperation()))
mulDagElement.data.tempValueA = 0.0
mulDagElement.data.valueB = 4.0

dag = Dag()
dag.elements.append(addDagElement)
dag.elements.append(mulDagElement)


forwardBackwardLearning = ForwardBackwardLearning()
forwardBackwardLearning.dag = dag
forwardBackwardLearning.rateObject = TestRate(12.0)

for step in range(1000):
	forwardBackwardLearning.iteration()

	print(forwardBackwardLearning.rate(forwardBackwardLearning.dag))

"""
example:


              4 * ---- 12
6 ---- +  ----- 
? ----
"""
