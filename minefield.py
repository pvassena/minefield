#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlobject as SO
import random

__connection__ = SO.connectionForURI("mysql://minefield:password@localhost/MineField")
#__connection__.debug = True


class Mine(SO.SQLObject):
	x = SO.IntCol()
	y = SO.IntCol()
	chunk = SO.ForeignKey('Chunk')

class Chunk(SO.SQLObject):
	i = SO.IntCol()
	j = SO.IntCol()
	board = SO.ForeignKey('Board')
	mines = SO.MultipleJoin('Mine')

	def generate_mines(self):
		#generate square list
		squares = []
		for x in range( board.chunk_size ):
			for y in range( board.chunk_size ):
				squares.append( (x,y) )
		
		#get list of random squares
		mines = random.sample( squares, board.chunk_mines )
		
		#create mines in the squares
		for mine in mines:
			Mine( x=mine[0], y=mine[1], chunk=self )

class Board(SO.SQLObject):
	chunk_size = SO.IntCol()
	chunk_mines = SO.IntCol()
	chunks = SO.MultipleJoin('Chunk')

board = Board( chunk_size=8, chunk_mines=5 )
chunk = Chunk( i=0, j=0, board=board )
#chunk.generate_mines()
#for mine in Mine.select():
#	print(mine)
