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
  from Darwin import Darwin
  darwin = Darwin(offspring_num = 100,
                    generations = 50,
                    sizes=[20,21,27,4],
                    num_parents = 64,
                    mutation_rate = 7,
                    crossing_algorithm = "uniform",
                    saving_txt = True,
                    saving_csv = True,
                    saving_dna = True,
                    saveDnaThreshold = None,




                    cluster_id = "Darwin 1",
                    tty = None,              #If you want to redirect the
                                             #   output to a specific terminal,
                                             #  useful when dealing with threads.


                    loadDnaPath = "GenTests/Gen test - 2020-01-06 - 14:19:33-Darwin 1-2-109.0.npy") #Load parents from another training

  darwin.main()
  


