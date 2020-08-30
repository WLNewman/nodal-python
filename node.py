import pygame
import math
from dijkstra import dijkstra
pygame.init()
pygame.font.init()

hitbox = 12

class Node:
	def __init__(self, x, y, sisters, edges):
		#sisters are the nodes which share an edge
		#edges store weights, sisters/edges have same index
		self.x = x
		self.y = y
		self.sisters = sisters
		self.edges = edges
		self.distance = 999999999 #my infinity
		self.previousNode  = []

	def draw(self, color, win):
		if self.sisters != []:
			for sister in range(len(self.sisters)): #just the edge
				pygame.draw.aaline(win, (30, 100, 150), (self.x, self.y), (self.sisters[sister].getPos()), 1)
				f = ((self.x + self.sisters[sister].getPos()[0])*(1/2), (self.y + self.sisters[sister].getPos()[1])*(1/2))
				
				#the following used to be own function, but it only worked when in this function
				try: #displays edge weights
					value = pygame.font.SysFont('Tahoma', 10)
					number = value.render(f"{self.edges[sister]}", False, (255,255,255))
					cost = value.render(f"D={self.distance}", False, (255,0,255))
					win.blit(number, f) #just the edge weight
					if self.distance != 999999999:
						win.blit(cost, (self.x, self.y - 15)) #just the node distance
				except: #need this because I think nodal takes time to append edges
					pass#kept getting out of range error which this solved
		return pygame.draw.circle(win, color, (self.x, self.y), 5)

	def changePos(self, mouse):
		#takes in mouse position and sets Node to that
		if mouse == 0: #dummy amount for preventing overlapping nodes
			self.x += 20
		else:
			self.x = mouse[0]
			self.y = mouse[1]

	def getPos(self):
		return (self.x, self.y)
		
	def grab(self, mouse):
		#check if mouse hovering near node (uses distance formula)
		box = math.sqrt(((mouse[0] - (self.x + 5))**2) + (mouse[1] - (self.y + 5))**2)
		if box <= hitbox:
			self.changePos(mouse)
			return box

	def addEdge(self, sisCoords):
		#take in a node as a parameter and establish an edge between them
		if sisCoords.getPos() == self.getPos() or sisCoords in self.sisters:
			pass #this prevents self linking and repeat linking
		else:
			self.sisters.append(sisCoords)
			self.edges.append(1)
			

	def removeEdge(self, sister):
		try:
			pos = self.sisters.index(sister)
			self.sisters.remove(sister)
			self.edges.pop(pos)
		except:
			pass

	def changeWeight(self, sis, intg):
		try:	
			pos = self.sisters.index(sis)
			self.edges[pos] += intg
		except:
			pass

	def getWeight(self, sis):
		#find the weight of the sister sis
		pos = self.sisters.index(sis)
		return self.edges[pos]

	def setDistance(self, num):
		self.distance = num

	def findDistance(self):
		return self.distance

	def returnSisters(self):
		#gives sorted list of sisters to dijkstra
		sortedSisters = []
		for sis in self.sisters:
			sortedSisters.append(sis)
		#bubble sort bad, I know but there's only a few elements per list
		sorting = True
		while sorting and len(sortedSisters) > 1:
			sorting = False
			for s in range(len(sortedSisters) - 1):
				if self.getWeight(sortedSisters[s]) > self.getWeight(sortedSisters[s + 1]):
					sorting = True
					index1 = sortedSisters[s]
					index2 = sortedSisters[s+1]
					sortedSisters[s] = index2
					sortedSisters[s + 1] = index1
		return sortedSisters

	def setPrevious(self, prev):
		self.previousNode = prev

	def showPath(self, color, win):
		pygame.time.delay(100)
		if self.previousNode !=[]:
			pygame.draw.line(win, color, (self.getPos()[0], self.getPos()[1]), (self.previousNode.getPos()), 3)
			self.previousNode.showPath(color, win)
		else:
			self.draw((0,255,0), win)