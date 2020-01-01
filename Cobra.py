import pygame
import sys
import random
import numpy as np
from Intelect import *
from NeuralNetworkPlay import *


vec = pygame.Vector2

def keyboardControl(snake):
  keys = pygame.key.get_pressed()
  if keys[pygame.K_UP] and (snake.dir != 'down'):
    snake.dir = 'up'
  if keys[pygame.K_DOWN] and (snake.dir != 'up'):
    snake.dir = 'down'
  if keys[pygame.K_LEFT] and (snake.dir != 'right'):
    snake.dir = 'left'
  if keys[pygame.K_RIGHT] and (snake.dir != 'left'):
    snake.dir = 'right'

class Snake():
  def __init__(self,pos):
    self.dir = 'right' 
    self.body = [pos]
    self.color = (255,0,0)
    self.step = BLOCK_SIZE
    self.vel = vec(0,0)
    self.ub = False
    self.lb = False
    self.rb = False
    self.db = False
    self.selfCollided = False

  def selfCollision(self, member):
    if self.body[0] == member:
      self.selfCollided =  True

  def bodyBackPropagation(self, i):
    self.body[i].x = self.body[i-1].x
    self.body[i].y = self.body[i-1].y
  
  def dirControl(self):
    if self.dir == 'right':
      self.body[0].x += self.step
      self.vel = vec(self.step,0)
    if self.dir == 'left':
      self.body[0].x -= self.step
      self.vel = vec(-self.step, 0)
    if self.dir == 'up':
      self.body[0].y -= self.step
      self.vel = vec(0, -self.step)
    if self.dir == 'down':
      self.body[0].y += self.step
      self.vel = vec(0, self.step)

  def debug(self):
    #print("Head pos:", self.body[0])
    #print('Up:%s, Right:%s, Left:%s, Down: %s'%(self.ub,self.rb,self.lb,self.db))
    pass
  
  def draw(self, surface):
    for member in self.body:
      pygame.draw.rect(surface, self.color,
                                  (member.x,
                                   member.y,
                                   BLOCK_SIZE,
                                   BLOCK_SIZE))
  
  
  def foodCollision(self, game, snack):
    if self.body[0] == snack.pos:
      self.body.insert(0,vec(self.body[0]))
      snack.spawn(self)
      game.MOVES_LEFT = game.EXTRA_MOVES
  
    
  
  def neuralNetworkMove(self,input):
    if input == 0 and (self.dir != 'down'):
      self.dir = 'up'
    if input == 1 and (self.dir != 'up'):
      self.dir = 'down'
    if input == 2 and (self.dir != 'right'):
      self.dir = 'left'
    if input == 3 and (self.dir != 'left'):
        self.dir = 'right'

  def update(self, game, snack):
    for i,member in enumerate(self.body):
      if i > 0:
        self.bodyBackPropagation(len(self.body)-i)
      if i >= 3:
        self.selfCollision(member)
    self.dirControl()
    self.debug()
    self.foodCollision(game,snack)

class Food():
  def __init__(self):
    self.pos = vec(0,0)
    self.color = (0,255,0)

  def spawn(self,snake):
    while True:
      x = random.randint(0,(ROWS-1))*BLOCK_SIZE
      y = random.randint(0,(COLS-1))*BLOCK_SIZE
      if len(list(filter(lambda z : z == vec(x,y), snake.body))) > 0:
        continue
      else:
        break
    self.pos = vec(x,y)      

      
  
  def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                                (self.pos.x,
                                 self.pos.y,
                                 BLOCK_SIZE,
                                 BLOCK_SIZE))
    

class Game():
  def __init__(self,sizes = None, weights = None, tick = None, draw = False, keyboard = False):
    self.KEYBOARD = keyboard

    self.TICK = tick 
    self.DRAW = draw
    self.SIZES = sizes

    if self.DRAW:
      self.win = pygame.display.set_mode((WIDTH, WIDTH))
      self.clock = pygame.time.Clock()
    
    if self.SIZES:
      self.network = Network(sizes,weights)
    self.MOVES_LEFT = MOVES_LEFT
    self.EXTRA_MOVES = EXTRA_MOVES

    self.s = Snake(vec(WIDTH/2,WIDTH/2))
    self.snack = Food()
    self.snack.spawn(self.s)
    
  
  def events(self):
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

  def draw(self):
    self.win.fill((0,0,0))
    self.s.draw(self.win)
    self.snack.draw(self.win)
    pygame.display.update()



  def wallCollision(self):
    if self.s.body[0].x > WIDTH-BLOCK_SIZE or \
    self.s.body[0].x < 0                   or \
    self.s.body[0].y > WIDTH-BLOCK_SIZE    or \
    self.s.body[0].y < 0:
      #print("Wall collision!")
      return True


  def angle_with_apple(self):
    appleDirVec = np.array(self.snack.pos) - np.array(self.s.body[0])
    snakeDirVec = self.s.vel.x , self.s.vel.y 

    appleDirVecNorm = np.linalg.norm(appleDirVec)
    snakeDirVecNorm = np.linalg.norm(snakeDirVec)

    if appleDirVecNorm == 0:
        appleDirVecNorm = BLOCK_SIZE
    if snakeDirVecNorm == 0:
        snakeDirVecNorm = BLOCK_SIZE

    appleDirVecNormalized\
       = appleDirVec / appleDirVecNorm

    snakeDirVecNormalized\
       = snakeDirVec / snakeDirVecNorm

    return appleDirVecNormalized,snakeDirVecNormalized

  def isDirectionBlocked(self, direction):
    adjacentStep = self.s.body[0] + direction
    if adjacentStep in self.s.body:
      return 1
    else:
      if adjacentStep.x > WIDTH-BLOCK_SIZE:
        return 1
      if adjacentStep.x < 0:
        return 1
      if adjacentStep.y > WIDTH-BLOCK_SIZE:
        return 1
      if adjacentStep.y < 0:
        return 1
      return 0

     

  def blockedDirections(self):
    ub = self.isDirectionBlocked(vec(0,-BLOCK_SIZE))
    lb = self.isDirectionBlocked(vec(-BLOCK_SIZE,0))
    rb = self.isDirectionBlocked(vec(BLOCK_SIZE,0))
    db = self.isDirectionBlocked(vec(0,BLOCK_SIZE))
    return ub,lb,rb,db

  def handle_network_inputs(self):
    inputs = [[0],[0],[0],[0],[0],[0],[0],[0]]
    self.s.ub, self.s.lb, self.s.rb, self.s.db = self.blockedDirections()
    apple_angle, snake_dir_angle = self.angle_with_apple()
    inputs[0] = [self.s.ub]
    inputs[1] = [self.s.lb]
    inputs[2] = [self.s.rb]
    inputs[3] = [self.s.db]
    inputs[4] = [apple_angle[0]]
    inputs[5] = [apple_angle[1]]
    inputs[6] = [snake_dir_angle[0]]
    inputs[7] = [snake_dir_angle[1]]
    output = self.network.feedforward(inputs)
    return np.argmax(output)

  def gameOver(self,penaltyInput):
    score = len(self.s.body)*5000 - \
              penaltyInput - \
              1500/len(self.s.body)
    return score, len(self.s.body)


  def main(self):
    while True:
      if self.TICK:
        self.clock.tick(self.TICK)
      self.s.update(self,self.snack)
      if self.DRAW: 
        self.draw()
        self.events()
      if self.KEYBOARD:
        keyboardControl(self.s)
      if self.MOVES_LEFT <= 0:
        return self.gameOver(-10)
      if self.s.selfCollided:
        return self.gameOver(-150)
      if self.wallCollision():
        return self.gameOver(-150)
      self.MOVES_LEFT -= 1
      #self.s.ub, self.s.lb, self.s.rb, self.s.db = self.blockedDirections()
      
      if self.SIZES:
        output = self.handle_network_inputs()
        self.s.neuralNetworkMove(output)
  
  

