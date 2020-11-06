#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlobject as SO
import random
__connection__ = SO.connectionForURI("mysql://minefield:password@localhost/MineField")
#__connection__.debug = True


class Mine(SO.SQLObject):
	class sqlmeta:
		style = SO.MixedCaseStyle( longID=True )
	x = SO.IntCol()
	y = SO.IntCol()
	Chunk = SO.ForeignKey('Chunk')

class Chunk(SO.SQLObject):
	class sqlmeta:
		style = SO.MixedCaseStyle( longID=True )
	i = SO.IntCol()
	j = SO.IntCol()
	Board = SO.ForeignKey('Board')

	def generate_mines(self):
		board = Board.select( Board.q.id==self.Board ).getOne()
		
		#generate square list
		squares = []
		for x in range( board.ChunkSize ):
			for y in range( board.ChunkSize ):
				squares.append( (x,y) )
		
		#get list of random squares
		mines = random.sample( squares, board.ChunkMines )
		
		#create mines in the squares
		for mine in mines:
			Mine( x=mine[0], y=mine[1], Chunk=self.id )

class Board(SO.SQLObject):
	class sqlmeta:
		style = SO.MixedCaseStyle( longID=True )
	ChunkSize = SO.IntCol()
	ChunkMines = SO.IntCol()

board = Board(ChunkSize=8, ChunkMines=5 )
chunk = Chunk( i=0, j=0, Board=board.id )
chunk.generate_mines()
for mine in Mine.select():
	print(mine)
