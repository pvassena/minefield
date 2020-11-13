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
	k = SO.IntCol()
	board = SO.ForeignKey('Board')
	mines = SO.MultipleJoin('Mine')
	
	def generate_mines(self):
		#generate square list
		squares = set()

		while len(squares)<self.board.chunk_mines:
			x = random.randrange(self.board.chunk_size)
			y = random.randrange(self.board.chunk_size)
			squares.add( (x,y) )

		#create mines in the squares
		for square in squares:
			Mine( x=square[0], y=square[1], chunk=self )
	
	def get_mines_around(self, x, y):
		counter = 0
		#check chunk mines
		for mine in self.mines:
			if abs(mine.x-x)<=1 and abs(mine.y-y)<=1:
				if not (mine.x==x and mine.y==y):
					counter += 1
		#check left mines
		if x==0:
			chunk=self.board.get_chunk( i=self.i-1, k=self.k)
			for mine in chunk.mines:
				if mine.x==self.board.chunk_size-1 and abs(mine.y-y)<=1:
					counter += 1
		#check right mines
		if x==self.board.chunk_size-1:
			chunk=board.get_chunk(i=self.i+1, k=self.k)
			for mine in chunk.mines:
				if mine.x==0 and abs(mine.y-y)<=1:
					counter += 1
		#check up mines
		if y==0:
			chunk=board.get_chunk(i=self.i, k=self.k-1)
			for mine in chunk.mines:
				if abs(mine.x-x)<=1 and mine.y==self.board.chunk_size-1:
					counter += 1
		#check down mines
		if y==self.board.chunk_size-1:
			chunk=board.get_chunk(i=self.i, k=self.k+1)
			for mine in chunk.mines:
				if abs(mine.x-x)<=1 and mine.y==0:
					counter += 1
		#check left_up mines
		if x==0 and y==0 :
			chunk=self.board.get_chunk( i=self.i-1, k=self.k-1)
			for mine in chunk.mines:
				if mine.x==self.board.chunk_size-1 and mine.y==self.board.chunk_size-1:
					counter += 1
		#check right_up mines
		if x==self.board.chunk_size-1 and y==0:
			chunk=board.get_chunk(i=self.i+1, k=self.k-1)
			for mine in chunk.mines:
				if mine.x==0 and  mine.y==self.board.chunk_size-1:
					counter += 1
		#check left_down mines
		if x==0 and y==self.board.chunk_size-1:
			chunk=board.get_chunk(i=self.i-1, k=self.k+1)
			for mine in chunk.mines:
				if mine.x==self.board.chunk_size-1 and mine.y==0:
					counter += 1
		#check right_down mines
		if x==self.board.chunk_size-1 and y==self.board.chunk_size-1:
			chunk=board.get_chunk(i=self.i+1, k=self.k+1)
			for mine in chunk.mines:
				if mine.x==0 and mine.y==0:
					counter += 1
		return counter
	
	def print(self):
		display=[]
		for y in range( self.board.chunk_size ):
			display.append([])
			for x in range( self.board.chunk_size ):
				display[y].append(self.get_mines_around(x,y))
		for mine in self.mines:
			display[mine.y][mine.x]='█'
		
		for x in range( self.board.chunk_size ):
			for y in range( self.board.chunk_size ):
				print( display[x][y], end='')
			print()

class Board(SO.SQLObject):
	chunk_size = SO.IntCol()
	chunk_mines = SO.IntCol()
	chunks = SO.MultipleJoin('Chunk')
	
	def get_chunk(self, i, k):
		for chunk in self.chunks:
			if chunk.i==i and chunk.k==k:
				return chunk
		chunk = Chunk( i=i, k=k, board=self)
		chunk.generate_mines()
		return chunk

board = Board( chunk_size=5, chunk_mines=10 )
chunk = board.get_chunk(0,-1)
chunk.print()
chunk = board.get_chunk(0,0)
chunk.print()
chunk = board.get_chunk(0,1)
chunk.print()
