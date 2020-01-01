#Config
WIDTH = 200
BLOCK_SIZE = 20
ROWS = WIDTH/BLOCK_SIZE
COLS = ROWS
EXTRA_MOVES = 100
MOVES_LEFT = 100

if __name__ == "__main__":
  from Darwin import Darwin
  darwin = Darwin(offspring_num = 100,
                    generations = 50,
                    view_generations = 1000,
                    sizes=[8,9,15,4],
                    num_parents = 12,
                    mutation_rate = 5,
                    crossing_algorithm = "uniform",
                    cluster_id = "Darwin 1",
                    saving_txt = True,
                    saving_csv = True,
                    saving_dna = True)  
  darwin.main()

