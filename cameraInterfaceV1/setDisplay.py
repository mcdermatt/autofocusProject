import sys
import os
import pygame
from time import sleep

pygame.init()

clock = pygame.time.Clock()

scrsize = width,height = 720,480
black = 0,0,0
bgcolor = (240,240,220) #light grey

fullscreen_sz = pygame.display.Info().current_w, pygame.display.Info().current_h
print("screen size= ", fullscreen_sz)

screen = pygame.display.set_mode(scrsize, pygame.FULLSCREEN)

font = pygame.font.SysFont( 'arial,microsoftsanserif,corier',20)

txt2display = font.render('blah blah blah', True, black)
txt2display_w = txt2display.get_size()[0]

screen.fill(bgcolor)
screen.blit(txt2display, ((scrsize[0]+1-txt2display_w)//2,1))
pygame.display.update()

#clock.tick(60)
sleep(10)
