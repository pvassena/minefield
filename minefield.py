#!/usr/bin/python3

from sqlobject_minefield import *
import pygame as PG

board = Board ( chunk_size=5, chunk_mines=20 )
chunk = board.get_chunk(i=0, k=0)

#init pygame modules
PG.init()

#init some variables
tile = 40
#colors
black = (0,0,0)
gray = (100,100,100)
red = (255,0,0)
#screen
screen = PG.display.set_mode((tile*15,tile*15))
PG.display.set_caption('MineField')
#font
font = PG.font.Font( PG.font.get_default_font(), 30) 

texts = []
for i in range(9):
    text = font.render( str(i), False, (0,255,0) )
    rect = text.get_rect()
    texts.append( {'text':text, 'rect':rect} )

def render_screen(i):
    screen.fill(black)

    for x in range(15):
        for y in range(15):
            texts[(x+i)%9]['rect'].centerx = x*tile+tile/2
            texts[(x+i)%9]['rect'].centery = y*tile+tile/2
                    
            screen.blit( texts[(x+i)%9]['text'], texts[(x+i)%9]['rect'] )
                    
            rect = PG.Rect((x*tile, y*tile), (tile, tile))
            PG.draw.rect(   surface = screen,
                            color = gray,
                            rect = rect,
			    width = 1,
			    border_radius = 7)
    PG.display.flip()

i = 0
while 1:
    render_screen(i)
    i+=1
    i%=9

