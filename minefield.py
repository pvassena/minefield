#!/usr/bin/python3

from sqlobject_minefield import *
import pygame as PG

size=5

board = Board ( chunk_size=size, chunk_mines=size )

#init pygame modules
PG.init()

#init some variables
tile = 40
#colors
black =     (  0,  0,  0)
gray =      (100,100,100)
red =       (255,  0,  0)
yellow =    (255,255,  0)
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

def render_screen():
    screen.fill(black)
    i_actual=0
    k_actual=0
    for i in range(i_actual-1, i_actual+2):
        for k in range(k_actual-1, k_actual+2):
            chunk = board.get_chunk(i,k)
            display = chunk.get_display()
            for x in range( size ):
                for y in range( size ):
                    if display[y][x]['is_hidden']==True:
                        pass
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
    rect = PG.Rect ((tile*size,tile*size),
                    (tile*size,tile*size))
    PG.draw.rect(   surface=screen,
                    color = red,
                    rect = rect,
                    width = 1,
                    border_radius = 0)
    PG.display.flip()

while 1:
    
    for event in PG.event.get():
        if event.type == PG.QUIT:
            quit()
        if event.type == PG.MOUSEBUTTONUP:
            pass
        if event.type == PG.KEYDOWN:
            if event.key == PG.K_ESCAPE:
                quit()
    render_screen()
