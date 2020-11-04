#!/usr/bin/python3

import random

def get_empty_square():
	square = {
		'Mine' : False,
		'Status' : 'Hidden'
	}
	return square

def get_empty_chunk(size):
	chunk = []
	for x in range(size):
		chunk.append([])
		for y in range(size):
			chunk[x].append( get_empty_square() )
	return chunk

def generate_mines(chunk, N):
	while N > 0:
		x = random.randrange(0, len(chunk[0]) )
		y = random.randrange(0, len(chunk[0]) )
		if chunk[x][y]['Mine'] == False:
			chunk[x][y]['Mine'] = True
			N -= 1

def print_chunk(chunk):
	for x in range( len(chunk[0]) ):
		for y in range( len(chunk[0]) ):
			if chunk[x][y]['Mine'] == True:
				print("X", end="")
			else:
				print("0", end="")
		print()

chunk=get_empty_chunk(3)
generate_mines(chunk,3)
print_chunk(chunk)

