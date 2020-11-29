#!/usr/bin/python3

from sqlobject_minefield import *
import pygame as PG
import datetime

arrow_keys = {
	PG.K_UP : 'UP',
	PG.K_DOWN : 'DOWN',
	PG.K_LEFT : 'LEFT',
	PG.K_RIGHT : 'RIGHT',
	PG.K_SPACE : 'RESET'
}

class Game():

	def __init__(self):
		self.current_i = 0
		self.current_k = 0
		self.board = Board( chunk_size=8 , chunk_mines=13 )
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
	
	def get_display(self):
		display = []
		for k in range(-1, 2):
			row = []
			for i in range(-1, 2):
				chunk = game.board.get_chunk(	i = i + self.current_i,
												k = k + self.current_k )
				row.append( chunk.get_display() )
			display.append( row )
		return display

class Render():

	def __init__(self, size):
		
		#init pygame modules
		PG.init()
		
		#set tile size in pixels
		self.tile = 40
		
		#set border dimension
		self.border = 2

		#set board size
		self.size = size
		
		#get a display
		self.screen = PG.display.set_mode( (self.tile*(self.size+2*self.border),
											self.tile*(self.size+2*self.border)) )
		
		#set display title
		PG.display.set_caption('MineField')
		
		#get a font
		self.font = PG.font.Font( PG.font.get_default_font(), 30) 
		
		#create a dictionary of blittable cell types
		self.cell = dict()
		
		#add empty cero
		self.cell[0] = self.blittable( '', (0, 0, 0) )

		#add yellow numbers
		for i in range(1,9):
			self.cell[i] = self.blittable( i, (200, 200, 0) )
		
		#add red X
		self.cell['X'] = self.blittable( 'X', (255, 0, 0) )
		
		#add green delta
		self.cell['Δ'] = self.blittable( 'Δ', (0, 255, 0) )
	
	def blittable(self, char, color):

		#create blittable surface
		surf = PG.Surface( (self.tile, self.tile) )
		rect_surf = surf.get_rect()

		#draw gray rectangle to surface
		PG.draw.rect(	surface = surf,
						color = (100, 100, 100), #gray
						rect = rect_surf,
						width = 1,
						border_radius = 7)

		#render text (this function doesn't accept named parameters)
		text = self.font.render(	str(char),		#text
									False,			#antialias
									color )			#color
		
		#center text in surface
		rect_text = text.get_rect()
		rect_text.centerx = rect_surf.centerx
		rect_text.centery = rect_surf.centery

		#blit text to surface
		surf.blit(	source = text,
					dest = rect_text )
		
		return surf

	def draw_cell(self, square, x_pos, y_pos ):
		if square['is_hidden'] == True:
			if square['flag'] == True:
				self.screen.blit( self.cell['Δ'], (x_pos, y_pos) )
		elif square['is_mine'] == True:
			self.screen.blit( self.cell['X'], (x_pos, y_pos) )
		else:
			self.screen.blit( self.cell[square['count']], (x_pos, y_pos) )

	def render_screen(self, i_actual, k_actual):
		self.screen.fill( (0, 0, 0) )
		for i in range(-1, +2):
			for k in range(-1, +2):
				chunk = game.board.get_chunk( i+i_actual, k+k_actual )
				display = chunk.get_display()
				for x in range( self.size ):
					for y in range( self.size ):
						self.draw_cell( square = display[y][x],
										x_pos = self.tile*(x+self.size*i+self.border),
										y_pos = self.tile*(y+self.size*k+self.border))


		rect = PG.Rect ((self.tile*self.border-1,self.tile*self.border-1),
						(self.tile*self.size+2,self.tile*self.size+2))
		PG.draw.rect(   surface=self.screen,
						color = (255,0,0),
						rect = rect,
						width = 1,
						border_radius = 8)
		PG.display.flip()

#main loop

game = Game()
render = Render(game.board.chunk_size)

while 1:
	
	render.render_screen(game.current_i, game.current_k)
	
	for event in PG.event.get():
		if event.type == PG.QUIT:
			quit()

		if event.type == PG.MOUSEBUTTONUP:
			x = (event.pos[0]//render.tile)-render.border
			y = (event.pos[1]//render.tile)-render.border
			if x>=0 and x<render.size:
				if y>=0 and y < render.size:
					if event.button == 1:
						game.dig_square( x=x, y=y )
					elif event.button == 3:
						game.switch_flag( x=x, y=y )

		if event.type == PG.KEYDOWN:
			if event.key in arrow_keys:
				game.change_chunk( arrow_keys[event.key] )
			elif event.key == PG.K_ESCAPE:
				print("thanks for playing")
				quit()






















