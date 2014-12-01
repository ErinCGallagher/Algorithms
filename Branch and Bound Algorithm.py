#Erin Gallagher (10054506)

from random import randrange
import copy
class MinHeap:
	
	#heap contained in a list
	#each parent P's children are at position i*2 and i*2+1
	#position 0 is filled with a 0 place holder
	def __init__(self):
		self.heapList = [0]
		self.currentSize = 0
	
	def moveUp(self,i):
		#loop until you have reached the top node of the min heap
		while i // 2 > 0:
			#sor by lower lowerBound
			if self.heapList[i].lowerBound < self.heapList[i // 2].lowerBound:
				#print "lowerBounds not equal"
				temp = self.heapList[i // 2]
				self.heapList[i // 2] = self.heapList[i]
				self.heapList[i] = temp
			#lowerBounds are equal
			elif self.heapList[i].lowerBound == self.heapList[i // 2].lowerBound:
				#sort by lower upperBound
				if self.heapList[i].upperBound < self.heapList[i // 2].upperBound:
					#print "lowerBounds equal, upperBounds not"
					temp = self.heapList[i // 2]
					self.heapList[i // 2] = self.heapList[i]
					self.heapList[i] = temp
				#upperBounds are equal
				elif self.heapList[i].upperBound == self.heapList[i // 2].upperBound:
					#sort by lenth of decisions made so far
					if len(self.heapList[i].pair) < len(self.heapList[i // 2].pair):
						#print "upperBounds equal, heapLists not"
						temp = self.heapList[i // 2]
						self.heapList[i // 2] = self.heapList[i]
						self.heapList[i] = temp
			i = i // 2
	
	#move a node from the top of the heap down to its correct position
	def moveDown(self,i):
		#move tdown the tree swaping the node in question with smaller nodes
		while (i * 2) <= self.currentSize:
			minimumC = self.minChild(i)
			#check to see if node is larger than the one below it 
			if self.heapList[i].lowerBound > self.heapList[minimumC].lowerBound:
				#swap nodes
				temp = self.heapList[i]
				self.heapList[i] = self.heapList[minimumC]
				self.heapList[minimumC] = temp
			i = minimumC
	
	#determines which of the 2 children nodes is smaller
	def minChild(self,i):
		#if there is not right child return the left child
		if i * 2 + 1 > self.currentSize:
			return i * 2
		else:#return the smaller child node
			if self.heapList[i*2].lowerBound < self.heapList[i*2+1].lowerBound:
				return i * 2
			else:
				return i * 2 + 1
	
	#removes the mimum node from the heap and reheapifies
	def removeMin(self):
		minimum = self.heapList[1]
		self.heapList[1] = self.heapList[self.currentSize]
		self.currentSize = self.currentSize - 1
		self.heapList.pop()
		self.moveDown(1)
		return minimum
	
	#build heap from scratch		
	def buildHeap(self,list):
		i = len(list) // 2
		self.currentSize = len(list)
		self.heapList = list
		while (i > 0):
			  self.moveDown(i)
			  i = i - 1
		
	#add a node to the heap
	def addToHeap(self,element):
		self.currentSize+=1 #increase current size
		i = self.currentSize
		self.heapList.append(element)
		 #move the item from the bottom of the heap to correct position
		self.moveUp(i)
			  
	def printHeap(self):
		for i in range(1,self.currentSize):
			print self.heapList[i].lowerBound 

#defines a partial solution
class Node:
	def __init__(self, cSF, gFC, lowerBound, upperBound,chosen,pair):
		self.cSF = cSF #cost so far
		self.gFC = gFC #guanranteed future cost
		self.lowerBound = lowerBound #csf + gfc
		self.upperBound = upperBound #csf + feasible solution
		self.chosen = chosen #list of rows and cols defining the reduced matrix
		self.pair = pair #list of decisions made so far
	
	#adds a decision to the list of decisions made so far
	def addPair(self,newPair):
		self.pair.append(newPair)
	
	#prints the list of decisions made so far
	def printList(self):
		print "decisions:"
		for i in self.pair:
			print i
		print "end decisions"
		print ""




bh = MinHeap()


#read in the file and return the size and entries matrix
def openFile():
	global input
	
	with open("lab2Input25.txt","r") as file:
		entries = []
		lines = file.readlines()
		for i in range(1, int(lines[0])+1):
			entries.append(map(int, lines[i].split()))
	return entries, int(lines[0])
#end openFile
	

#global UpperBound option 1: random selection
def upperCalc(chosen):
	global entries
	upperBound = 0
	
	for i in chosen[0]: #go through the rows
		#select a random column and then remove it from options
		
		choice = randrange(len(chosen[1])) #choose index of next choice
		selection = chosen[1][choice]
		chosen = removeChoice(chosen, choice) #remove choice from list
		upperBound += entries[i][selection]
		
	return upperBound
#end upperCalc


#removes a choice and returns a new chosen list
#for gloabl UpperBound option 1
def removeChoice(chosen, choice):
	newChosen = copy.deepcopy(chosen)
	del newChosen[1][choice]
	return newChosen
#end removeChoice

'''
#global  UpperBound option2: select the diagonal
def upperCalc(chosen):
	global entries
	upperBound = 0
	
	for i in range(0, len(chosen[0])): #go through the rows
		#select the associated diagonal
		upperBound += entries[chosen[0][i]][chosen[1][i]]
		
	return upperBound
#end upperCalc
'''

#lower Bound option 1: min in each row
#chosen is a list of lists with number of still available [rows][columns] of entries
def lowerCalc(chosen):
	global entries
	lowerBound = 0
	
	#find the min number in each row
	for row in chosen[0]:
		#set min default to first element in the row
		min = entries[row][chosen[1][0]]
		for col in chosen[1]:
			if entries[row][col] < min:
				min = entries[row][col]
		lowerBound += min
	return lowerBound
#end lowerCalc
"""

#lowerBound option2: row reduction
#reduce the rows and columns to determine the gfc
def lowerCalc(chosen):
	minimums = [[],[]] #store reduction results
	
	#determine the min number is each row and store it in minimums
	for row in chosen[0]:
		lowerCalc=entries[row][chosen[1][0]]
		for col in chosen[1]:
			if entries[row][col] < lowerCalc:
				lowerCalc = entries[row][col]
		minimums[0].append(lowerCalc)
	
	#find the min number in each column
	for col in chosen[1]:
		rowCount = 0 
		minCol = entries[1][col]-minimums[0][rowCount]
		for row in chosen[0]:#subtract the reduced row values of column values
			rowReduced = entries[row][col]-minimums[0][rowCount]
			if rowReduced< minCol:
				minCol = rowReduced
			rowCount +=1
		minimums[1].append(minCol)
	
	#iterate through reduction results to find total gcf
	total = 0
	for row in minimums[0]:
		total +=row
	for col in minimums[1]:
		total +=col
	return total

#end rowReduction
"""
#create list of partial solutions/nodes from current state		
def decisions(node):
	global upperBound
	global bh
	global size
	global partialSolutionCount
	global entries
	
	list = []
	chosen = node.chosen
	#select the first row from reduced matrix
	#go through each available column and create a node if valid
	for col in chosen[1]:
		partialSolutionCount +=1
		
		csf = node.cSF + entries[chosen[0][0]][col]
		pair = (chosen[0][0], col)
		
		#remove your choice from the chosen list (reduce matrix)
		newChosen = copy.deepcopy(chosen)
		newChosen[0].remove(chosen[0][0])
		newChosen[1].remove(col)
		
		#if you are on your last decision, gfc is 0
		if len(node.pair) < size-1:
			gfc = lowerCalc(newChosen)
		else: #last decision
			gfc =0
			
		lowerBound = csf +gfc
		
		#calculate new upperBound and change global is lower
		newUpperBound = csf +  upperCalc(newChosen)
		if newUpperBound < upperBound:
			upperBound = newUpperBound
		
		#ensure lowerBound is less than or equal to upperBoud
		if lowerBound <= upperBound:
			oldDecisions = copy.deepcopy(node.pair)
			node1 = Node(csf,gfc,lowerBound,newUpperBound,newChosen, oldDecisions)
			node1.addPair(pair)
			bh.addToHeap(node1)
	
#end decisions


#choose min off top of the heap
def makeSelection(size):	
	global bh
	global upperBound
	
	node = bh.removeMin()
	#if the lowerBound is greater than your global upperBound
	while node.lowerBound > upperBound:
		print"NODE NOT SELECTED DUE TO HIGH LOWER BOUND"
		node = bh.removeMin()

	print ""
	print"node selected ", node.pair[-1]
	#node.printList()

	if len(node.pair) == size:
		print "SOLUTION: "
		print "final csf ", node.cSF
		node.printList()
		print "lowerBound ", node.lowerBound
		return 0
		
	return node
#end makeSelection


#create the initial chosen list with the total rows and cols of the matrix
#chosen = [[rows][cols]]
def createChosen(size):
	chosen = [[],[]]
	for i in range(0,size):
		chosen[0].append(i)
		
	for i in range(0,size):
		chosen[1].append(i)
	return chosen
#end createChosen


#MAIN

#open file
entries, size = openFile()
#create the chosen list that characterises your reduced matrix
chosen = createChosen(size)
upperBound = upperCalc(chosen) #create upper bound

partialSolutionCount  = 0

selectedNode = Node(0,0,0,0,chosen,[])

while selectedNode != 0:
	decisions(selectedNode)
	selectedNode = makeSelection(size)

print "PARTIAL SOLUTION COUNT ", partialSolutionCount
print "DONE"



