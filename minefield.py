#!/usr/bin/python3

import sys
from sqlobject_minefield import *
from game import *
from render import *
import pygame as PG
import time

arrow_keys = {
	PG.K_UP : 'UP',
	PG.K_DOWN : 'DOWN',
	PG.K_LEFT : 'LEFT',
	PG.K_RIGHT : 'RIGHT',

	PG.K_SPACE : 'RESET',
	
	PG.K_w : 'UP',
	PG.K_s : 'DOWN',
	PG.K_a : 'LEFT',
	PG.K_d : 'RIGHT'
}

#main loop

if len(sys.argv) > 1:
	game = Game(board = int(sys.argv[1]))
else:
	game = Game()

render = Render(game.board.chunk_size)

while 1:
	render.render_screen(	displays = game.get_displays(1000000000000),
							board = game.board.id,
							score = game.get_score(),
							mines = game.board.chunk_mines - game.count_flags())

	if game.get_gameover():
		render.render_gameover()
		time.sleep(2)
		quit()

	for event in PG.event.get():
		if event.type == PG.QUIT:
			quit()

		if event.type == PG.MOUSEBUTTONUP:
			square = render.get_square( event.pos )
			if square:
				if event.button == 1:
					game.dig_square( x=square[0], y=square[1] )
				elif event.button == 3:
					game.switch_flag( x=square[0], y=square[1] )

		if event.type == PG.KEYDOWN:
			if event.key in arrow_keys:
				game.change_chunk( arrow_keys[event.key] )
			elif event.key == PG.K_ESCAPE:
				quit()
