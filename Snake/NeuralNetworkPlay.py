#Config
WIDTH = 900
BLOCK_SIZE = 90
ROWS = WIDTH/BLOCK_SIZE
COLS = ROWS
EXTRA_MOVES = 100
MOVES_LEFT = 100

"""
Main build:
  offspring_num = 2000,
  generations = 500,
  view_generations = 64,
  sizes=[20,21,27,4],
  num_parents = 64,
  mutation_rate = 7,
  crossing_algorithm = "uniform",
"""

if __name__ == "__main__":
  import sys
  sys.path.append("../Nature")
  from Darwin import Evolution
  from Cobra import *

                    
  evolve = Evolution( 


    # Hyperparameters
    offspring_num = 100,
    generations = 500,
    sizes=[20,21,27,4],
    num_parents = 12,
    mutation_rate = 7,
    crossing_algorithm = "uniform",

    # Saving
    saving_txt = True,
    saving_csv = True,
    saving_dna = True,
    saveDnaThreshold = None,

    #  If you want to redirect the
    #  output to a specific terminal,
    #  useful when dealing with threads.
    cluster_id = "Darwin 1",
    tty = None,              

    #Load parents from another training
    loadDnaPath = "",
    game = Game) 

  evolve.main()
  


