#!/usr/bin/python3

import pygame as PG

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

	def render_screen(self, displays):
		self.screen.fill( (0, 0, 0) )
		k=-1
		for row in displays:
			i=-1
			for display in row:
				for x in range( self.size ):
					for y in range( self.size ):
						self.draw_cell( square = display[y][x],
										x_pos = self.tile*(x+self.size*i+self.border),
										y_pos = self.tile*(y+self.size*k+self.border))
				i += 1
			k += 1


		rect = PG.Rect ((self.tile*self.border-1,self.tile*self.border-1),
						(self.tile*self.size+2,self.tile*self.size+2))
		PG.draw.rect(   surface=self.screen,
						color = (255,0,0),
						rect = rect,
						width = 1,
						border_radius = 8)
		PG.display.flip()
