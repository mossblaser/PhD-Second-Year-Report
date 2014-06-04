#!/usr/bin/env python2

import random

import sys

SEED         = int(sys.argv[1])
WIDTH        = int(sys.argv[2])
HEIGHT       = int(sys.argv[3])
CROP         = int(sys.argv[4])
SCALE        = float(sys.argv[5])
NUM_NEURONS  = int(sys.argv[6])
NUM_CON      = int(sys.argv[7])
PROB_THRESH  = float(sys.argv[8])
NEURON_SHIFT = float(sys.argv[9])

random.seed(SEED)


# List of (x,y, [targets]) where targets are (x,y) pairs. Insert one token
# central one which be our example neuron
neurons = [(WIDTH/2, HEIGHT/2, [])]

# Produce a random set of neurons
for n in range(NUM_NEURONS):
	while True:
		x = random.randrange(0,WIDTH-1)
		y = random.randrange(0,HEIGHT-1)
		if (x, y, []) not in neurons:
			neurons.append((x,y, []))
			break

# Randomly connect neurons
for x,y, connections in neurons:
	possible_connections = neurons[:]
	random.shuffle(possible_connections)
	for _ in range(NUM_CON):
		for x2,y2,_ in possible_connections:
			weight = (float((x-x2)**2 + (y-y2)**2) / (WIDTH**2 + HEIGHT**2)) ** 0.5
			if PROB_THRESH > weight and (x2,y2) not in connections:
				connections.append((x2,y2))
				break

print r"\begin{tikzpicture}[scale=%f,inner sep=0]"%SCALE

print r"\tikzset{example/.style={ultra thin},nonexample/.style={ultra thin}}"

print r"\clip (%d,%d) rectangle (%d,%d);"%(CROP, CROP, WIDTH-CROP, HEIGHT-CROP)
print r"\begin{pgfonlayer}{background}"
print r"\clip (%d,%d) rectangle (%d,%d);"%(CROP, CROP, WIDTH-CROP, HEIGHT-CROP)
print r"\end{pgfonlayer}"

print r"\draw (0,0) rectangle ++(%d,%d);"%(WIDTH,HEIGHT)

# Neuron positions
for x,y,_ in neurons:
	x_pos = x + random.gauss(0.0, NEURON_SHIFT)
	y_pos = y + random.gauss(0.0, NEURON_SHIFT)
	print r"\node (neuron %d %d) at (%f,%f) {};"%(x, y, x_pos, y_pos)

# Synapses
for x,y,connections in neurons:
	for x2,y2 in connections:
		if (x,y) == (WIDTH/2, HEIGHT/2):
			print r"\draw [example] (neuron %d %d) -- (neuron %d %d);"%(x,y, x2,y2)
		else:
			print r"\begin{pgfonlayer}{background}"
			print r"\draw [nonexample] (neuron %d %d) -- (neuron %d %d);"%(x,y, x2,y2)
			print r"\end{pgfonlayer}"

# Neurons
for x,y,_ in neurons:
	if (x,y) == (WIDTH/2, HEIGHT/2):
		print r"\node [fill,circle,minimum width=0.8ex,example] at (neuron %d %d) {};"%(x,y)
	else:
		print r"\begin{pgfonlayer}{background}"
		print r"\node [nonexample,fill,circle,minimum width=0.8ex] at (neuron %d %d) {};"%(x,y)
		print r"\end{pgfonlayer}"

print r"\end{tikzpicture}"
