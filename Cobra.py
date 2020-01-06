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
    self.selfCollided = False

  def selfCollision(self):
    for member in self.body[2:]:
      if self.body[0] == member:
        return True

  def bodyBackPropagation(self, i):
    self.body[i].x = self.body[i-1].x
    self.body[i].y = self.body[i-1].y
  
  def dirControl(self):
    if self.dir == 'right':
      self.body[0].x += BLOCK_SIZE
      self.vel = vec(BLOCK_SIZE,0)
    if self.dir == 'left':
      self.body[0].x -= BLOCK_SIZE
      self.vel = vec(BLOCK_SIZE, 0)
    if self.dir == 'up':
      self.body[0].y -= BLOCK_SIZE
      self.vel = vec(0, -BLOCK_SIZE)
    if self.dir == 'down':
      self.body[0].y += BLOCK_SIZE
      self.vel = vec(0, BLOCK_SIZE)

  def debug(self):
    #print("Head pos:", self.body[0])
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
      if vec(x,y) in snake.body:
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
      return True

  
  def normalizeVector(self,dirVec):
    dirVecNorm = np.linalg.norm(dirVec)

    if dirVecNorm == 0:
      dirVecNorm = BLOCK_SIZE
    dirVecNormalized = dirVec / dirVecNorm

    return dirVecNormalized

  def isDirectionBlocked(self, direction):
    adjacentStep = self.s.body[0] + direction
    if adjacentStep in self.s.body:
      bodyBlock = 1
    else:
      bodyBlock = 0
    if adjacentStep.x > WIDTH-BLOCK_SIZE or \
      adjacentStep.x < 0                 or \
      adjacentStep.y > WIDTH-BLOCK_SIZE  or \
      adjacentStep.y < 0:
      wallBlock = 1
    else:
      wallBlock = 0
      
    return bodyBlock, wallBlock

     

  def blockedDirections(self):
    ubb,uwb = self.isDirectionBlocked(vec(0,-BLOCK_SIZE))
    lbb,lwb = self.isDirectionBlocked(vec(-BLOCK_SIZE,0))
    rbb,rwb = self.isDirectionBlocked(vec(BLOCK_SIZE,0))
    dbb,dwb = self.isDirectionBlocked(vec(0,BLOCK_SIZE))
    ubb2,uwb2 = self.isDirectionBlocked(vec(0,-2*BLOCK_SIZE))
    lbb2,lwb2 = self.isDirectionBlocked(vec(-2*BLOCK_SIZE,0))
    rbb2,rwb2 = self.isDirectionBlocked(vec(2*BLOCK_SIZE,0))
    dbb2,dwb2 = self.isDirectionBlocked(vec(0,2*BLOCK_SIZE))
    return uwb,lwb,rwb,dwb,uwb2,lwb2,rwb2,dwb2,\
           ubb,lbb,rbb,dbb,ubb2,lbb2,rbb2,dbb2,

  def handle_network_inputs(self):
    inputs = [ [0] for x in range(self.SIZES[0])]
    uwb, lwb, rwb, dwb, uwb2, lwb2, rwb2, dwb2, \
    ubb, lbb, rbb, dbb, ubb2, lbb2, rbb2, dbb2 = self.blockedDirections()

    apple_angle = self.normalizeVector\
                          (np.array(self.snack.pos) - \
                           np.array(self.s.body[0]))

    snake_dir_angle = self.normalizeVector\
                          ((self.s.vel.x , self.s.vel.y))
    

    inputs[0] = [uwb]
    inputs[1] = [lwb]
    inputs[2] = [rwb]
    inputs[3] = [dwb]
    inputs[4] = [uwb2]
    inputs[5] = [lwb2]
    inputs[6] = [rwb2]
    inputs[7] = [dwb2]
    inputs[8] = [ubb]
    inputs[9] = [lbb]
    inputs[10] = [rbb]
    inputs[11] = [dbb]
    inputs[12] = [ubb2]
    inputs[13] = [lbb2]
    inputs[14] = [rbb2]
    inputs[15] = [dbb2]
    inputs[16] = [apple_angle[0]]
    inputs[17] = [apple_angle[1]]
    inputs[18] = [snake_dir_angle[0]]
    inputs[19] = [snake_dir_angle[1]]
    output = self.network.feedforward(inputs)
    return np.argmax(output)

  def gameOver(self,penaltyInput):
    score = len(self.s.body)*5000 - \
              penaltyInput - \
              1500/len(self.s.body)
    return score, len(self.s.body)

  def youWon(self):
    score = len(self.s.body)*5000
    print("You Won!")
    return score, len(self.s.body)

  def main(self):
    while True:
      if len(self.s.body) >= 100:
        return self.youWon()
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
      if self.s.selfCollision():
        return self.gameOver(-150)
      if self.wallCollision():
        return self.gameOver(-150)

      self.MOVES_LEFT -= 1
      
      if self.SIZES:
        output = self.handle_network_inputs()
        self.s.neuralNetworkMove(output)
  
  

