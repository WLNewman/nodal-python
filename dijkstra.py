import pygame
import math

def dijkstra(nodeList, window, source, target):
	pygame.display.update()
	win = window
	win.fill((0,0,0))
	for node in nodeList:
		if node == source:
			node.setDistance(0)
	keepThisListToDraw = []

	while nodeList != []:
		minDist = 1000000000
		activeNode = 'x'
		for node in nodeList:  
			if node.findDistance() < minDist:
				minDist = node.findDistance()
				activeNode = node
		keepThisListToDraw.append(activeNode)
		nodeList.remove(activeNode)
#fixed glitch where any node as source besides original
#would end up competing with original to reach target.
#I was removing active node in the loop, so many were
#removed by mistake. Also explains why some nodes never lit up
		pygame.time.delay(125)
		for node in keepThisListToDraw:
			if node == source:
				node.draw((0,0,255), win)
			else:
				node.draw((255,0,255), win)

		activeNode.showPath((149,80,75), window)

		pygame.display.update()
		win.fill((0,0,0))

		sis = activeNode.returnSisters()
		for n in sis:
			#if n in nodeList:
			altPath = activeNode.findDistance() + activeNode.getWeight(n)
			if altPath <= n.findDistance():
				n.setDistance(altPath)
				n.setPrevious(activeNode)

	for node in keepThisListToDraw:
		node.draw((0,0,0), win)
	target.draw((0,255,0), win)
	target.showPath((80, 100, 20), win)
	pygame.display.update()
	win.fill((0,0,0))
	#pygame.time.delay(500)
	print(f"Final: {target.findDistance()}\n\n")
	pygame.time.delay(6000)

	#need to do this to reset distances
	for node in keepThisListToDraw:
		node.setDistance(999999999)
		node.setPrevious([])
