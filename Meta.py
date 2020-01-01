from ClassDarwin import Darwin


darwin = Darwin(offspring_num = 200,
                  generations = 100,
                  view_generations = 30,
                  sizes=[8,9,15,4],
                  num_parents = 100,
                  mutation_rate = 25,
                  crossing_algorithm = "uniform",
                  cluster_id = "Darwin 1",
                  draw = True,
                  tick = 1000)  

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

