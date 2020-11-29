#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlobject as SO
import random
import datetime

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
		size = self.board.chunk_size
		#generate square list
		squares = set()

		while len(squares)<self.board.chunk_mines:
			x = random.randrange( size )
			y = random.randrange( size )
			squares.add( (x,y) )

		#create mines in the squares
		for square in squares:
			Mine( x=square[0], y=square[1], chunk=self )
	
	def get_display(self):
		size = self.board.chunk_size
		#generate display grid
		display=[]
		for y in range( size ):
			display.append([])
			for x in range( size ):
				display[y].append( {'is_mine':False, 'count':0, 'is_hidden':True, 'flag':False} )
		#check self mines
		for mine in self.mines:
			display[mine.y][mine.x]['is_mine']=True
			for x in range(mine.x-1 ,mine.x+2):
				for y in range(mine.y-1 ,mine.y+2):
					if x>=0 and x<size and y>=0 and y<size:
						display[y][x]['count'] += 1
		#check left mines
		chunk=self.board.get_chunk( i=self.i-1, k=self.k)
		mines = Mine.selectBy( chunk = chunk, x = size-1 )
		for mine in mines:
			for y in range(mine.y-1 ,mine.y+2):
				if y>=0 and y<size:
					display[y][0]['count'] += 1
		#check right mines
		chunk=self.board.get_chunk( i=self.i+1, k=self.k)
		mines = Mine.selectBy( chunk = chunk, x = 0 )
		for mine in mines:
			for y in range(mine.y-1 ,mine.y+2):
				if y>=0 and y<size:
					display[y][size-1]['count'] += 1
		#check up mines
		chunk=self.board.get_chunk( i=self.i, k=self.k-1)
		mines = Mine.selectBy( chunk = chunk, y = size-1 )
		for mine in mines:
			for x in range(mine.x-1 ,mine.x+2):
				if x>=0 and x<size:
                                    display[0][x]['count'] += 1
		#check down mines
		chunk=self.board.get_chunk( i=self.i, k=self.k+1)
		mines = Mine.selectBy( chunk = chunk, y = 0 )
		for mine in mines:
			for x in range(mine.x-1 ,mine.x+2):
				if x>=0 and x<size:
					display[size-1][x]['count'] += 1
		#check left_up mines
		chunk=self.board.get_chunk( i=self.i-1, k=self.k-1 )
		mine = Mine.selectBy( chunk = chunk, x = size-1, y = size-1 )
		if mine.count():
			display[0][0]['count'] += 1
		#check right_up mines
		chunk=self.board.get_chunk( i=self.i+1, k=self.k-1 )
		mine = Mine.selectBy( chunk = chunk, x = 0, y = size-1 )
		if mine.count():
			display[0][size-1]['count'] += 1
		#check left_down mines
		chunk=self.board.get_chunk( i=self.i-1, k=self.k+1 )
		mine = Mine.selectBy( chunk = chunk, x = size-1, y = 0 )
		if mine.count():
			display[size-1][0]['count'] += 1
		#check right_down mines
		chunk=self.board.get_chunk( i=self.i+1, k=self.k+1 )
		mine = Mine.selectBy( chunk = chunk, x = 0, y = 0 )
		if mine.count():
			display[size-1][size-1]['count'] += 1
		#set non hidden mines
		actions = Action.selectBy( chunk=self )
		for action in actions:
			if action.action == 'DIG':
				display[action.y][action.x]['is_hidden']=False
			else:
				display[action.y][action.x]['flag'] = not display[action.y][action.x]['flag']
		return display

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

class Action(SO.SQLObject):
	x = SO.IntCol()
	y = SO.IntCol()
	chunk = SO.ForeignKey('Chunk')
	time = SO.TimestampCol()
	action = SO.EnumCol(enumValues=['DIG','SWITCH_FLAG'])
