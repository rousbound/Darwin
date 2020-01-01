#Config
WIDTH = 200
BLOCK_SIZE = 20
ROWS = WIDTH/BLOCK_SIZE
COLS = ROWS
EXTRA_MOVES = 100
MOVES_LEFT = 100

if __name__ == "__main__":
  from ClassDarwin import Darwin
  darwin = Darwin(offspring_num = 200,
                    generations = 100,
                    view_generations = 1000,
                    sizes=[8,9,15,4],
                    num_parents = 24,
                    mutation_rate = 10,
                    crossing_algorithm = "uniform",
                    cluster_id = "Darwin 1",
                    saving_txt = True,
                    saving_csv = True,
                    saving_dna = True)  

  """darwin2 = Darwin(offspring_num = 200,
                    generations = 100,
                    view_generations = 50,
                    sizes=[8,9,15,3],
                    num_parents = 100,
                    mutation_rate = 25,
                    crossing_algorithm = "singlepoint",
                    cluster_id = "Darwin 2",
                    draw = False,
                    tick = None)  """

  darwin.main()

