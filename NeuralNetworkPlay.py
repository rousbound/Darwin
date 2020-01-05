#Config
WIDTH = 900
BLOCK_SIZE = 90
ROWS = WIDTH/BLOCK_SIZE
COLS = ROWS
EXTRA_MOVES = 100
MOVES_LEFT = 100

"""
Main build:
  offspring_num = 200,
  generations = 500,
  view_generations = 1000,
  sizes=[8,9,15,4],
  num_parents = 24,
  mutation_rate = 5,
  crossing_algorithm = "uniform",
"""

if __name__ == "__main__":
  from Darwin import Darwin
  import threading
  darwin = Darwin(offspring_num = 400,
                    generations = 500,
                    view_generations = 1000,
                    sizes=[8,9,15,4],
                    num_parents = 12,
                    mutation_rate = 5,
                    crossing_algorithm = "uniform",
                    cluster_id = "Darwin 1",
                    saving_txt = True,
                    saving_csv = True,
                    saving_dna = True,
                    saveDnaThreshold = 90,
                    tty = None)  

  """darwin2 = Darwin(offspring_num = 200,
                    generations = 50,
                    view_generations = 1000,
                    sizes=[8,9,15,4],
                    num_parents = 24,
                    mutation_rate = 2,
                    crossing_algorithm = "uniform",
                    cluster_id = "Darwin 2",
                    saving_txt = True,
                    saving_csv = True,
                    saving_dna = True,
                    tty = 4)  """
  darwin.main()
  
"""
  d1 = threading.Thread(target = darwin.main) 
  d2 = threading.Thread(target = darwin2.main) 
  d1.start()
  d2.start()
"""


