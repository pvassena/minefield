#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlobject as SO
import random

__connection__ = SO.connectionForURI("mysql://minefield:password@localhost/MineField")
__connection__.debug = True


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
		for x in range( self.board.chunk_size ):
			for y in range( self.board.chunk_size ):
				squares.append( (x,y) )
		
		#get list of random squares
		mines = random.sample( squares, self.board.chunk_mines )
		
		#create mines in the squares
		for mine in mines:
			Mine( x=mine[0], y=mine[1], chunk=self )

	def get_mines_around(self, x, y):
		counter = 0
		#check chunk mines
		for mine in self.mines:
			if abs(mine.x-x)<=1 and abs(mine.y-y)<=1:
				if not (mine.x==x and mine.y==y):
					counter += 1
		#check left mines
		if x==0:
			chunk=self.board.get_chunk( i=self.i-1, j=self.j-1)
			for mine in chunk.mines:
				if mine.x==self.board.chunk_size and abs(mine.y-y)<=1:
					counter += 1
		#check right mines
		if x==self.board.chunk_size:
			chunk=board.get_chunk(i=self.i+1, j=self.j)
			for mine in chunk.mines:
				if mine.x==0 and abs(mine.y-y)<=1:
					counter += 1
		#check up mines
		if y==0:
			chunk=board.get_chunk(i=self.i, j=self.j-1)
			for mine in chunk.mines:
				if abs(mine.x-x)<=1 and mine.y==self.board.chunk_size:
					counter += 1
		#check down mines
		if y==self.board.chunk_size:
			chunk=board.get_chunk(i=self.i, j=self.j+1)
			for mine in chunk.mines:
				if abs(mine.x-x)<=1 and mine.y==0:
					counter += 1	
		return counter	
	
	def print(self):
		display=[]
		for x in range( self.board.chunk_size ):
			display.append([])	
			for y in range( self.board.chunk_size ):
				display[x].append(self.get_mines_around(x,y))
		for mine in self.mines:
			display[mine.x][mine.y]='█'

		for x in range( self.board.chunk_size ):	
			for y in range( self.board.chunk_size ):
				print( display[x][y], end='')
			print()
						
class Board(SO.SQLObject):
	chunk_size = SO.IntCol()
	chunk_mines = SO.IntCol()
	chunks = SO.MultipleJoin('Chunk')
	
	def get_chunk(self, i, j):
		for chunk in self.chunks:
			if chunk.i==i and chunk.j==j:
				return chunk
		chunk=Chunk( i=i, j=j, board=self)
		chunk.generate_mines()
		return chunk
	
board = Board( chunk_size=8, chunk_mines=1 )
chunk = board.get_chunk(0,0)
chunk.print()
