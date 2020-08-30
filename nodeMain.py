import pygame
import math
from node import Node
from dijkstra import dijkstra

dimension = 500
white = (255, 255, 255)
edge = (30, 100, 150)
path = (150, 100, 30)

win = pygame.display.set_mode((dimension, dimension))
pygame.display.set_caption("nodal")

nodeList = []
node1 = Node(250,250, [], [])
nodeList.append(node1)

running = True

while(running):
	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		#1.) add node event 2.) join two existing nodes event
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				arr = pygame.mouse.get_pos()
				temp = Node(arr[0], arr[1], [], [])
				nodeList.append(temp)
				node1.addEdge(temp)
				temp.addEdge(node1)
			if event.button == 3:
				for node in nodeList:
					if node.grab(pygame.mouse.get_pos()):
						node1.addEdge(node)
						node.addEdge(node1)

		#add weight to node event
		if keys[pygame.K_RIGHT]:
			for node in nodeList:
				if node.grab(pygame.mouse.get_pos()):
					node1.changeWeight(node, 1)
					node.changeWeight(node1, 1)

		#remove weight from node event
		if keys[pygame.K_LEFT]:
			for nodeA in nodeList:
				if nodeA.grab(pygame.mouse.get_pos()):
					node1.changeWeight(nodeA, -1)
					nodeA.changeWeight(node1, -1)

		#move node event, prevent overlapping event
		if keys[pygame.K_LSHIFT]:
			for nodeA in nodeList:
				if nodeA.grab(pygame.mouse.get_pos()):
					node1 = nodeA
				for nodeB in nodeList: #if nodeA and nodeB aren't the same node
					if nodeA != nodeB:             #and if they have identical coordinates change that
						if nodeA.getPos() == nodeB.getPos():
							nodeA.changePos(0)

		#remove node, remove edge game event
		if keys[pygame.K_SPACE]:
			if node1.grab(pygame.mouse.get_pos()) and len(nodeList) > 1:
				for node in nodeList:
					node.removeEdge(node1)
				nodeList.remove(node1)
				node1 = nodeList[0]
			for nodeA in nodeList:
				if nodeA.grab(pygame.mouse.get_pos()):
					node1.removeEdge(nodeA)
					nodeA.removeEdge(node1)
		
		#activate dijkstra event
		if keys[pygame.K_d]:
			nodeCopy = []
			for node in nodeList:
				nodeCopy.append(node)
			for node in nodeCopy:
				if node.grab(pygame.mouse.get_pos()):
					dijkstra(nodeCopy, win, node1, node)
#WHY>?>
		if keys[pygame.K_ESCAPE]:
			running = False

	for node in nodeList:
		if node == node1:
			node.draw(path, win)
		else:
			node.draw(white, win)

	pygame.display.update()
	win.fill((0, 0, 0))