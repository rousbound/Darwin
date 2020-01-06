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
  darwin = Darwin(offspring_num = 100,
                    generations = 500,
                    view_generations = 1000,
                    sizes=[12,13,19,4],
                    num_parents = 12,
                    mutation_rate = 6,
                    crossing_algorithm = "uniform",
                    cluster_id = "Darwin 1",
                    saving_txt = True,
                    saving_csv = True,
                    saving_dna = True,
                    saveDnaThreshold = 85,
                    tty = None,
                    loadDnaPath = "GenTests/GoodDna/Gen test - 2020-01-05 - 18:02:56-Darwin 1-3-97.0.npy")  

  darwin.main()
  


