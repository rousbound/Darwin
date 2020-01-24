#!/usr/bin/env python
# -*-coding=utf-8 -*-
import pygame, math, random
import time
from settings import *
from neuralNetworkPlay import *
from player import Player
from column import Column
from Intelect import Network
import sys

class Game():
    def __init__(self, weights = None, sizes = None, gameArgs = None):
        self.SIZES = sizes
        self.fps = None
        self.timer = time.clock()
        if gameArgs:
            self.fps = gameArgs['fps']
        if self.fps:
            self.clock = pygame.time.Clock()
            self.win = pygame.display.set_mode((winw,winh))
        if self.SIZES:
            self.network = Network(sizes = sizes, weights = weights)
    
        self.player = Player(100,100, self.SIZES) 
        self.COLUMN_SPACING = 300
        self.lColumns = [Column(self.COLUMN_SPACING+x) for x in range(100,winw+self.COLUMN_SPACING,self.COLUMN_SPACING)]
        self.score = 0
        pass

    def spawnColumns(self):
        for i,col in enumerate(self.lColumns):
          col.x -= self.player.vel.x
          if col.x <= -col.size:
            self.score += 1
            del self.lColumns[0]
            self.lColumns.append(Column(self.lColumns[-1].x + self.COLUMN_SPACING))
          if(pygame.Rect.colliderect(self.player.rect,col.rectTop) or \
             pygame.Rect.colliderect(self.player.rect,col.rectBottom)):
            return True
        return False

    def debug_mode(self):
        pass

    def fps_counter(self):
      self.clock.tick(self.fps)
      self.win_caption = pygame.display.set_caption("Game title    FPS:%d"%self.clock.get_fps())

    def draw_screen(self):
        self.win.fill((0,0,0))
        self.player.draw(self)
        for col in self.lColumns:
          col.draw(self)
        pygame.display.update()

    def update(self):
        self.player.update()
        for col in self.lColumns:
          col.update()

        if self.SIZES:
            self.player.neuralControl\
                (self.player.neuralThink\
                  (self.lColumns, self))
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                run = False
        if self.fps:
            self.player.keyboardControl()
            self.fps_counter()

    def main(self):
      while True:
        if self.fps:
          self.draw_screen()
          self.events()
        self.update()
        if self.spawnColumns():
          break
        if self.player.pos.y > winh:
          break 
        if self.player.pos.y < 0 - self.player.block_size:
          break
        if self.score > 200:
          print("You won!")
          break

      now = time.clock()
      return  self.score / (now - self.timer), self.score
        


