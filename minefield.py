#!/usr/bin/python3

from sqlobject_minefield import *
import pygame as PG
import datetime

arrow_keys = {
	PG.K_UP : 'UP',
	PG.K_DOWN : 'DOWN',
	PG.K_LEFT : 'LEFT',
	PG.K_RIGHT : 'RIGHT'
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
		Action( chunk = self.chunk,
				x = x,
				y = y,
				action = 'DIG',
				time = datetime.datetime.now() )
	
	def get_display(self):
		pass

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
		self.screen = PG.display.set_mode( (self.tile*(self.size*3),
											self.tile*(self.size*3)) )
		
		#set display title
		PG.display.set_caption('MineField')
		
		#get a font
		self.font = PG.font.Font( PG.font.get_default_font(), 30) 
		
		#create a list of possible cell types
		printable = [str(i) for i in range(9)]
		printable.append('X')
		printable.append('Δ')
		
		#create a dictionary of blittable cell types
		self.cell = dict()
		for char in printable:
			
			#create blittable surface
			surf = PG.Surface( (self.tile, self.tile) )
			rect_surf = surf.get_rect()

			#draw gray rectangle to surface
			PG.draw.rect(	surface = surf,
							color = (100, 100, 100), #gray
							rect = rect_surf,
							width = 1,
							border_radius = 7)

			#render text
			text = self.font.render(	char,			#text
										False,			#antialias
										(200, 200, 0) ) #color = yellow
			
			#center text in surface
			rect_text = text.get_rect()
			rect_text.centerx = rect_surf.centerx
			rect_text.centery = rect_surf.centery

			#blit text to surface
			surf.blit(	source = text,
						dest = rect_text )
			
			#add surface to dictionary
			self.cell[char] = surf
	
	def render_screen(self, i_actual, k_actual):
		self.screen.fill( (0, 0, 0) )
		for i in range(-1, +2):
			for k in range(-1, +2):
				chunk = game.board.get_chunk( i+i_actual, k+k_actual )
				display = chunk.get_display()
				for x in range( self.size ):
					for y in range( self.size ):
						if display[y][x]['is_hidden']==True:
							if display[y][x]['flag']==True:
								self.screen.blit( self.cell['Δ'], ( self.tile*(x+self.size*(i+1)), self.tile*(y+self.size*(k+1)) ) )
						elif display[y][x]['is_mine']==True:
							self.screen.blit( self.cell['X'],  ( self.tile*(x+self.size*(i+1)), self.tile*(y+self.size*(k+1)) ) )
						else:
							count = display[y][x]['count']
								
							self.screen.blit( self.cell[str(count)], (x*self.tile+self.tile*self.size*(i+1), y*self.tile+self.tile*self.size*(k+1)) )
						
		rect = PG.Rect ((self.tile*self.size-1,self.tile*self.size-1),
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
			if event.pos[0]//render.tile//render.size == 1 and event.pos[1]//render.tile//render.size == 1:	
				x = (event.pos[0]//render.tile)%render.size
				y = (event.pos[1]//render.tile)%render.size
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






















