from ClassDarwin import Darwin


darwin = Darwin(offspring_num = 100,
                  generations = 50,
                  view_generations = 1000,
                  sizes=[8,9,15,4],
                  num_parents = 12,
                  mutation_rate = 5,
                  crossing_algorithm = "uniform",
                  cluster_id = "Darwin 1",
                  draw = False,
                  tick = 100,
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

