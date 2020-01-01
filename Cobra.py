#Snake Tutorial Python

import math
import random
import pygame
import sys
from Intelect import*

pygame.init()

class cube(object):
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0), VEL = 20):
        self.BLOCK_SIZE = VEL
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color


    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx*self.BLOCK_SIZE, self.pos[1] + self.dirny*self.BLOCK_SIZE)

    def draw(self, surface):
        dis = self.BLOCK_SIZE
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i,j, dis, dis))




class snake(object):
    def __init__(self, color, pos, VEL):
      self.BLOCK_SIZE = VEL
      self.body = []
      self.turns = {}
      self.color = color
      self.head = cube(pos)
      self.body.append(self.head)
      self.dirnx = 0
      self.dirny = 1

    def move(self,input):

        left = self.dirny,-self.dirnx
        right= -self.dirny,self.dirnx

        if input == 0:
            self.dirnx,self.dirny = left
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif input == 1:
            self.dirnx,self.dirny = self.dirnx,self.dirny
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif input == 2:
            self.dirnx,self.dirny = right
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]


        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)





    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube( 
                              (tail.pos[0] - self.BLOCK_SIZE,
                                tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube( 
                              (tail.pos[0] + self.BLOCK_SIZE,
                                tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube( 
                              (tail.pos[0],
                                tail.pos[1] - self.BLOCK_SIZE)))
        elif dx == 0 and dy == -1:
            self.body.append(cube( 
                              (tail.pos[0],
                                tail.pos[1] + self.BLOCK_SIZE)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw_s(self, surface):
        for c in self.body:
            c.draw(surface)




class Game():
    def __init__(self,sizes,weights= None,tick = None, draw = False,delay=None):
        self.WIDTH = 1000
        self.BLOCK_SIZE = 20
        self.win = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        self.rows = self.BLOCK_SIZE

        self.s = snake((255,0,0), (self.WIDTH/2,self.WIDTH/2),self.BLOCK_SIZE)
        self.snack = cube(self.randomSnack(self.rows, self.s), color=(0,255,0))
        self.network = Network(sizes,weights)

        self.MOVES_LEFT = 100

        self.draw = draw
        self.delay = delay
        self.clock = pygame.time.Clock()
        self.tick = tick

        self.prev_mov = 0
        self.penalty = 0
        self.count_same_mov = 0

    def angle_with_apple(self):
        apple_direction_vector = np.array(self.snack.pos) - np.array(self.s.head.pos)
        snake_direction_vector = self.s.head.dirnx * self.BLOCK_SIZE, self.s.head.dirny * self.BLOCK_SIZE

        norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
        norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)

        if norm_of_apple_direction_vector == 0:
            norm_of_apple_direction_vector = self.BLOCK_SIZE
        if norm_of_snake_direction_vector == 0:
            norm_of_snake_direction_vector = self.BLOCK_SIZE

        apple_direction_vector_normalized
           = apple_direction_vector / norm_of_apple_direction_vector

        snake_direction_vector_normalized 
           = snake_direction_vector / norm_of_snake_direction_vector
                                                                                 
        return apple_direction_vector_normalized,snake_direction_vector_normalized


    def collision_with_boundaries(self,next_step):
        if next_step[0] >= self.WIDTH or\
           next_step[0] < 0           or\
           next_step[1] >= self.WIDTH or\
           next_step[1] <0:

            return 1
        else:
            return 0

    def collision_with_self(self,next_step):
        body_pos=[]
        for block in self.s.body[1:]:
            body_pos.append(block.pos)
            if block.pos[0] == next_step[0] and\
               block.pos[1] == next_step[1]:
                return 1
            else:
                return 0

    def is_direction_blocked(self,direction):

        next_step = (self.s.head.pos[0] + direction[0]*self.BLOCK_SIZE,\
                     self.s.head.pos[1] + direction[1]*self.BLOCK_SIZE)

        if self.collision_with_boundaries(next_step) == 1 or\
           self.collision_with_self(next_step)       == 1:
            return 1
        else:
            return 0

    def blocked_directions(self):
        front_blocked = self.is_direction_blocked((0,-1))
        left_blocked = self.is_direction_blocked((-1,0))
        right_blocked = self.is_direction_blocked((1,0))
        down_blocked = self.is_direction_blocked((0,1))
        return front_blocked,left_blocked,right_blocked,down_blocked

    def handle_network_inputs(self):
        inputs = [[0],[0],[0],[0],[0],[0],[0],[0]]
        fb,lb,rb,db = self.blocked_directions()
        apple_angle, snake_dir_angle = self.angle_with_apple()
        inputs[0] = [fb]
        inputs[1] = [lb]
        inputs[2] = [rb]
        inputs[3] = [db]
        inputs[4] = [apple_angle[0]]
        inputs[5] = [apple_angle[1]]
        inputs[6] = [snake_dir_angle[0]]
        inputs[7] = [snake_dir_angle[1]]
        output = self.network.feedforward(inputs)
        return np.argmax(output)


    def redrawWindow(self,surface):
        surface.fill((0,0,0))
        self.snack.draw(surface)
        self.s.draw_s(surface)
        pygame.display.update()


    def randomSnack(self,rows, item):
        positions = item.body
        while True:
            x = random.randrange(0,
                                  self.WIDTH - self.BLOCK_SIZE,
                                    self.BLOCK_SIZE)
            y = random.randrange(0,
                                  self.WIDTH - self.BLOCK_SIZE,
                                    self.BLOCK_SIZE)
            if len(
                  list(
                    filter(
                      lambda z : z.pos == (x,y) , positions ))) > 0:
                continue
            else:
                break

        return (x,y)

    def return_score(self,penaltyInput):
        score = len(self.s.body)*5000 -\
                 penaltyInput -\
                self.penalty -\
                 1500/len(self.s.body)
        return score,len(self.s.body)

    def main(self):
        while True:
            if self.tick:
                self.clock.tick(self.tick)
            if self.delay:
                pygame.time.delay(self.delay)

            self.MOVES_LEFT -=1
            move = self.handle_network_inputs()

            # Repetitivity Penalty Control
            if move == self.prev_mov:
                self.count_same_mov += 1
            if self.count_same_mov > 8:
                self.penalty += 2
            self.prev_mov = move

            self.s.move(move)

            # Food Eaten
            if self.s.body[0].pos == self.snack.pos:
                self.s.addCube()
                self.MOVES_LEFT += 200
                self.snack = cube(self.randomSnack(self.rows, self.s), color=(0,255,0))


            #Exit Conditions

            # Collision with body Control
            for x in range(len(self.s.body)):
                if self.s.body[x].pos in list(map(lambda z:z.pos,self.s.body[x+1:])):
                    return self.return_score(-150)

            # Collision with map perimeter Control
            if (0 > self.s.head.pos[0])                               or\
                 (self.s.head.pos[0] > self.WIDTH-self.BLOCK_SIZE)    or\
               (0 > self.s.head.pos[1])                               or\
                 (self.s.head.pos[1] > self.WIDTH-self.BLOCK_SIZE):
                return self.return_score(-150)
            
            # Out of moves death penalty
            if self.MOVES_LEFT <= 0:
                return self.return_score(-10)

            # Rendering
            if self.draw == True:
                self.redrawWindow(self.win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)




#g = Game([9,10,10,4],tick = 1000, delay = 5,draw=True)
#g.main()
