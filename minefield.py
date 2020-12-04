#!/usr/bin/python3

from sqlobject_minefield import *
from game import *
from render import *
import pygame as PG


arrow_keys = {
	PG.K_UP : 'UP',
	PG.K_DOWN : 'DOWN',
	PG.K_LEFT : 'LEFT',
	PG.K_RIGHT : 'RIGHT',
	PG.K_SPACE : 'RESET'
}

#main loop

game = Game()
render = Render(game.board.chunk_size)

while 1:
	
	render.render_screen( game.get_displays(1000000000000) )
	
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
				game.repetition()	
				quit()
