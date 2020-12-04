#!/usr/bin/python3

from sqlobject_minefield import *
import datetime
from render import *
import time

class Game():

	def __init__(self, board=None):
		self.current_i = 0
		self.current_k = 0
		if board == None:
			self.board = Board( chunk_size=8 , chunk_mines=13 )
		else:
			self.board = board
		self.chunk = self.board.get_chunk(	i = self.current_i,
											k = self.current_k )

	def	change_chunk(self, direction):
		if direction == 'LEFT':
			self.current_i -= 1
		elif direction == 'RIGHT':
			self.current_i += 1
		elif direction == 'UP':
			self.current_k -= 1
		elif direction == 'DOWN':
			self.current_k += 1
		elif direction == 'RESET':
			self.current_i = 0
			self.current_k = 0
		else:
			print("invalid direction")
			quit()
		self.chunk = self.board.get_chunk(	i = self.current_i,
											k = self.current_k )

	def switch_flag(self, x, y):
		Action( chunk=self.chunk,
				x = x,
				y = y,
				action = 'SWITCH_FLAG',
				time = datetime.datetime.now()
				)

	def dig_square(self, x, y):
		if not Action.selectBy(chunk=self.chunk, x=x, y=y, action='DIG').count():
			Action( chunk = self.chunk,
					x = x,
					y = y,
					action = 'DIG',
					time = datetime.datetime.now() )
			display = self.chunk.get_display()
			if display[y][x]['count'] == 0:
				for y1 in range(y-1, y+2):
					for x1 in range(x-1, x+2):
						if not (x1 == x and y1 == y):
							if x1>=0 and x1<self.board.chunk_size:
								if y1>=0 and y1<self.board.chunk_size:
									self.dig_square(x1, y1)
	
	def get_displays(self, max_action):
		displays = []
		for k in range(-1, 2):
			row = []
			for i in range(-1, 2):
				chunk = self.board.get_chunk(	i = i + self.current_i,
												k = k + self.current_k )
				display = chunk.get_display()
				display = chunk.update_display(display, max_action)
				row.append( display )
			displays.append( row )
		return displays

	def repetition(self):
		render = Render(self.board.chunk_size)
		actions = Action.select(SO.AND(Chunk.q.board==self.board, Action.j.chunk))
		for action in actions:
			while action.chunk.i != self.current_i or action.chunk.k != self.current_k:
				if action.chunk.i < self.current_i:
					self.change_chunk('LEFT')
				elif action.chunk.i > self.current_i:
					self.change_chunk('RIGHT')
				elif action.chunk.k < self.current_k:
					self.change_chunk('UP')
				elif action.chunk.k > self.current_k:
					self.change_chunk('DOWN')
				time.sleep(0.25)
				
			render.render_screen( self.get_displays(action.id) )			
			time.sleep(0.5)
		
		
