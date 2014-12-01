#Erin Gallagher
#October 19th, 2014

input = []

def openFile():
	global input
	
	with open("lab1input.txt") as file:
		i = 0
		for line in file:
			line = line.rstrip()
			var = line.partition("\t")
			input.append((int(var[0]), int(var[2]),i))
			i = i+1
#end

#print the result in the correct format
def printList(list):
	for i in range(0, len(list)):
		print "Day " , len(list)-i, ": ", "Agency" ": ", list[i][2]," Value ", list[i][1]
#end
	

#list = input list without the first touple
#quick sor the list in order of the largest value
def sortInputValue(list): #O(nlogn)
	if list == []:
		return list
	else:
		pivot = list[0][1]
		left = sortInputValue([tup for tup in list[1:] if tup[1] > pivot ])
		right = sortInputValue([tup for tup in list[1:] if tup[1] <= pivot])
		return left + [list[0]] +right
	return list
#end sortInputValue

#loop through the total number of given days (20)
#loop through the list looking for the largest # dealine for that day 
#decrement the day on each iteration
def path(numDays, list):
	final = []
	total = 0
	for i in range(numDays,0,-1): #loop through days
		k = 0
		max = 0
		length = len(list)-1
		while k <=length: #looking for the largest dealine
			if list[k][0] >= i:
				max = list[k]
				k = length+1 #end while
			k = k+1
		if max == 0:
			final = final + ["rest"]
		else:
			final = final + [max]
			list.remove(max)
			total = total + max[1] 
	return final, total		
#end path()		

#Main
openFile()
list = sortInputValue(input[1:]) #sort bassed on highest value
final, total = path(input[0][0], list)
printList(final)
print "total ", total



