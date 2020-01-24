from settings import *
import pygame
import random

class Column():
  def __init__(self,x):
    self.x = x
    self.color = (255,255,255)
    self.size = 75
    self.holeSize = random.randint(175,400) #275
    self.offset = random.randint(1,winh-self.holeSize)
    self.rectTop = pygame.Rect(self.x,0,self.size,self.offset)
    self.rectBottom = pygame.Rect(self.x,self.offset+self.holeSize,self.size,winh-self.offset)

  def update(self):
    self.rectTop = pygame.Rect(self.x,0,self.size,self.offset)
    self.rectBottom = pygame.Rect(self.x,self.offset+self.holeSize,self.size,winh-self.offset)


  def draw(self,game):  
    pygame.draw.rect(game.win, self.color, self.rectTop)
    pygame.draw.rect(game.win, self.color, self.rectBottom)
    
