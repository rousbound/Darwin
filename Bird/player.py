import pygame
import numpy as np
from neuralNetworkPlay import *

class Player():
  def __init__(self,x,y, sizes = None):
    self.SIZES = sizes
    self.pos = vec(x,y)
    self.acc = vec(0,0)
    self.vel = vec(0,5)
    self.gravity = 0.5
    self.orig_vel = 5
    self.block_size = 75
    self.rect = pygame.Rect(self.pos.x, self.pos.y, self.block_size, self.block_size)
    self.isStrife = False


  def update(self):
    self.rect = pygame.Rect(self.pos.x, self.pos.y, self.block_size, self.block_size)
    if self.vel.x < self.orig_vel:
        self.vel.x = self.orig_vel
    if self.isStrife == False:
        self.acc.y = self.gravity
    else:
        self.acc.y = 0
        self.vel.y = 0
    if self.isStrife == True:
        if self.vel.x == self.orig_vel:
            self.acc.y = self.gravity
            self.isStrife = False
    self.vel.x *= 0.97
    self.vel += self.acc
    self.pos.y += self.vel.y
    

  def draw(self, game):
    pygame.draw.rect(game.win, (255,0,0), self.rect)

  def jump(self):
      self.isStrife = False
      self.vel.y -= 5
  def strife(self):
      self.vel.x += 5
      self.isStrife = True
  def dive(self):
      self.isStrife = False
      self.vel.y += 5
    
  def keyboardControl(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        self.jump()
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        self.dive()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        self.strife()


  def neuralThink(self,lColumns,game):
    inputs = [ [0] for x in range(self.SIZES[0])]
    inputs[0] = [self.pos.y]
    inputs[1] = [self.vel.y]
    inputs[2] = [self.vel.x]
    inputs[3] = [self.acc.y]
    inputs[4] = [lColumns[0].offset]
    inputs[5] = [lColumns[1].offset]
    inputs[6] = [lColumns[2].offset]
    inputs[7] = [lColumns[0].x]
    inputs[8] = [lColumns[1].x]
    inputs[9] = [lColumns[2].x]
    inputs[10] = [lColumns[0].holeSize]
    inputs[11] = [lColumns[1].holeSize]
    inputs[12] = [lColumns[2].holeSize]
    output = game.network.feedforward(inputs)
    return np.argmax(output)

  def neuralControl(self, controls):
    if controls == 0:
      pass
    elif controls == 1:
        self.jump()
    """elif controls == 2:
        self.dive()
    elif controls == 3:
        self.strife()"""
    
