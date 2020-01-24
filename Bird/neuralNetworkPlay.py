import numpy as np
import pygame
import sys

sys.path.append('../Nature')

winw = 1280
winh = 640
vec = pygame.math.Vector2


if __name__ == "__main__":
  from Darwin import Evolution
  from flappyBird import Game
                    
  evolve = Evolution( 
    offspring_num = 1000,
    generations = 500,
    sizes=[13,12,17,4],
    num_parents = 32,
    mutation_rate = 7,
    crossing_algorithm = "uniform",
    saving_txt = True,
    saving_csv = True,
    saving_dna = True,
    saveDnaThreshold = 25,
    game = Game,
    gameArgs = {'fps': False})
    

  evolve.main()
  


