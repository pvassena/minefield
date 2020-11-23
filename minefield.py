#!/usr/bin/python3

from sqlobject_minefield import *
import pygame as PG
import datetime

size=8

board = Board ( chunk_size=size, chunk_mines=10 )

#init pygame modules
PG.init()

#init some variables
tile = 40
#colors
black =	 (  0,  0,  0)
gray =	  (100,100,100)
red =	   (255,  0,  0)
yellow =	(255,255,  0)
#screen
screen = PG.display.set_mode( (tile*size*3, tile*size*3) )
PG.display.set_caption('MineField')
#font
font = PG.font.Font( PG.font.get_default_font(), 30) 

texts = []
for i in range(9):
	text = font.render( str(i), False, yellow )
	texts.append( {'text':text, 'rect':text.get_rect()} )

text = font.render( 'X', False, red )
X_text = {'text':text, 'rect':text.get_rect()}
text = font.render( 'A', False, red )
Flag_text = {'text':text, 'rect':text.get_rect()} 


i_actual=0
k_actual=0
def render_screen(i_actual, k_actual):
	screen.fill(black)
	for i in range(-1, +2):
		for k in range(-1, +2):
			chunk = board.get_chunk( i+i_actual, k+k_actual )
			display = chunk.get_display()
			for x in range( size ):
				for y in range( size ):
					if display[y][x]['is_hidden']==True:
						if display[y][x]['flag']==True:
							Flag_text['rect'].centerx = x*tile+tile*size*(i+1)+tile/2
							Flag_text['rect'].centery = y*tile+tile*size*(k+1)+tile/2
							
							screen.blit( Flag_text['text'], Flag_text['rect'] )
					elif display[y][x]['is_mine']==True:
						X_text['rect'].centerx = x*tile+tile*size*(i+1)+tile/2
						X_text['rect'].centery = y*tile+tile*size*(k+1)+tile/2

						screen.blit( X_text['text'], X_text['rect'] )
					else:
						count = display[y][x]['count']
						texts[count]['rect'].centerx = x*tile+tile*size*(i+1)+tile/2
						texts[count]['rect'].centery = y*tile+tile*size*(k+1)+tile/2
							
						screen.blit( texts[count]['text'], texts[count]['rect'] )
							
					rect = PG.Rect((0,0), (tile, tile))
					rect.centerx = x*tile+tile*size*(i+1)+tile/2
					rect.centery = y*tile+tile*size*(k+1)+tile/2
					PG.draw.rect(   surface = screen,
									color = gray,
									rect = rect,
						width = 1,
						border_radius = 7)
	rect = PG.Rect ((tile*size-1,tile*size-1),
					(tile*size+2,tile*size+2))
	PG.draw.rect(   surface=screen,
					color = red,
					rect = rect,
					width = 1,
					border_radius = 8)
	PG.display.flip()

render_screen(i_actual, k_actual)
while 1:
	
	for event in PG.event.get():
		if event.type == PG.QUIT:
			quit()
		if event.type == PG.MOUSEBUTTONUP:
			if event.button == 1 or event.button == 3:
				i = (event.pos[0]//tile)//size-1+i_actual
				k = (event.pos[1]//tile)//size-1+k_actual
				chunk = Chunk.selectBy(i=i, k=k, board=board).getOne()
				
				x = (event.pos[0]//tile)%size
				y = (event.pos[1]//tile)%size
				
				time = datetime.datetime.now()
				
				if event.button == 1:
					action = 'DIG'
				if event.button == 3:
					action = 'SWITCH_FLAG'
				Action( chunk=chunk, x=x, y=y, action=action, time=time )
				render_screen(i_actual, k_actual)
		
		if event.type == PG.KEYDOWN:
			if event.key == PG.K_ESCAPE:
				quit()
			if event.key == PG.K_UP:
				k_actual -= 1
			if event.key == PG.K_DOWN:
				k_actual += 1
			if event.key == PG.K_LEFT:
				i_actual -= 1
			if event.key == PG.K_RIGHT:
				i_actual += 1
			render_screen(i_actual, k_actual)
