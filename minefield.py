#!/usr/bin/python3

from sqlobject_minefield import *
import pygame as PG
import pygame.freetype 
board = Board ( chunk_size=5, chunk_mines=5 )

chunk = board.get_chunk(i=0, k=0)

chunk.print()

#init pygame modules
PG.init()
PG.freetype.init()

#init some variables
tile = 40
black = (0,0,0)
gray = (100,100,100)
red = (255,0,0)
transparent = (0,0,0,255)
screen = PG.display.set_mode((tile*15,tile*15))
PG.display.set_caption('MineField')
font = PG.freetype.Font(None, 30) 

while 1:
	screen.fill(black)

	for x in range(15):
		for y in range(15):
			rect = PG.Rect((x*tile, y*tile), (tile, tile))
			PG.draw.rect(	surface = screen,
					color = gray,
					rect = rect,
					width = 1,
					border_radius = 5)
			font.render_to(	surf=screen,
					dest = rect,  	
					text = '1',   	
					fgcolor = red,
					size = 30)
	PG.display.flip()
