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
		remaining_mines = board.ChunkMines 
		while remaining_mines>0:
			x = random.randrange( board.ChunkSize )
			y = random.randrange( board.ChunkSize )
			mine = Mine.selectBy( x=x, y=y, Chunk=self.id )
			if mine.count() == 0:
				Mine( x=x, y=y, Chunk=self.id)
				remaining_mines -= 1

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
