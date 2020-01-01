from NewCobra import *
import random
import pygame as pg

# Standard build
# OFFSPRING_NUM = 2000
# GENERATIONS = 200
# SIZES = [8,9,15,3]
# NUM_PARENTS = 100
# MUTATION_RATE = 25

class Darwin():
    def __init__(self,  
                  offspring_num = 2000,
                  generations = 200,
                  view_generations = 50,
                  sizes=[8,9,15,4], 
                  num_parents = 1000,
                  mutation_rate = 25,
                  crossing_algorithm = "uniform",
                  cluster_id = "Darwin 1",
                  draw = False,
                  tick = None):

        pg.init()                
        self.ID = cluster_id
        self.OFFSPRING_NUM = offspring_num  
        self.GENERATIONS = generations 
        self.VIEW_GENERATIONS = view_generations
        self.generation = 0
        self.SIZES = sizes           
        print(self.SIZES)
        self.NUM_PARENTS = num_parents
        self.MUTATION_RATE = mutation_rate   
        self.CROSSOVER_ALGORITHM = crossing_algorithm

        self.TICK_COPY = tick
        self.TICK = tick
        self.DELAY = None 
        self.DRAW = draw

        self.lInput = self.SIZES[0]
        self.lHidden = self.SIZES[1:-1]
        self.lOutput = self.SIZES[-1]
  
        self.total_weights = self.get_total_weights()
        self.population_shape = (self.OFFSPRING_NUM,self.total_weights)

        self.new_population             =            np.random.choice \
                              (np.arange(-1,1,step = 0.01),
                                              size = self.population_shape,
                                           replace = True)


    def get_total_weights(self):
        self.mult = [[x*y] for (x,y) in zip(self.SIZES[1:],self.SIZES[:-1])]
        self.total = 0
        for mulResult in self.mult:
            self.total += mulResult[0]
        return self.total

    def runCurrentGeneration(self,population):

        scores = np.empty(self.OFFSPRING_NUM)
        bodies = np.empty(self.OFFSPRING_NUM)
        

        for i,weight in enumerate(self.new_population):

            snakeLifeSpan                  =           Game\
                              (self.SIZES,
                                   weights = weight, 
                                      tick = self.TICK, 
                                      draw = self.DRAW, 
                                  keyboard = True)

            score, body = snakeLifeSpan.main()
            scores[i] = score
            bodies[i] = body

        return scores, bodies





    def getMaximums(self,score,body):
        # Copy this array because we're gonna modify it
        scores = score.copy() 
        bodies = body.copy()

        bestAncestorsIndexes = []

        maximum_score = np.zeros(self.NUM_PARENTS)
        maximum_body = np.zeros(self.NUM_PARENTS)

        # Get NUM_PARENTS number of maximum values 
        for parentIndex in range(self.NUM_PARENTS):

            max_score = np.max(scores)
            max_body = np.max(bodies)

            index_max_score = np.argmax(scores)
            index_max_body = np.argmax(bodies)

            # Take out the best from the gene pool
            # So we can capture the second best and so on...

            scores[index_max_score] = 0
            bodies[index_max_score] = -99999

            maximum_score[parentIndex] = max_score
            maximum_body[parentIndex] = max_body

            bestAncestorsIndexes.append(index_max_body)

        return maximum_score, maximum_body, bestAncestorsIndexes

    def copyParents(self,bestAncestorsIndexes):
        
        x_size = self.NUM_PARENTS
        y_size = self.new_population.shape[1]
        ndaParents = np.empty((x_size, y_size))
      
        # Copy NUM_PARENTS numbers to ndaParents
        for i,parent in enumerate(ndaParents):
            ndaParents[i] = self.new_population[bestAncestorsIndexes[i]]

        return ndaParents

    def uniformCrossover(self,parents,OFFSPRING_NUM):
        new_offspring = np.empty((OFFSPRING_NUM,parents.shape[1]))

        for children in range(OFFSPRING_NUM):
            while True:
                p1 = random.randrange(parents.shape[0])
                p2 = random.randrange(parents.shape[0])
                if p1 != p2:
                  for weight in range(self.new_population.shape[1]):
                    if random.uniform(0,1) < 0.5:
                        new_offspring[children,weight] = parents[p1,weight]
                    else:
                        new_offspring[children,weight] = parents[p2,weight]
                  break
        return new_offspring


    def singlePointCrossover(self,parents,OFFSPRING_NUM):
        new_offspring = np.empty((OFFSPRING_NUM,parents.shape[1]))
        for children in range(OFFSPRING_NUM):
            while True:
                p1 = random.randrange(parents.shape[0])
                p2 = random.randrange(parents.shape[0])
                if p1 != p2:
                  pivotPoint = random.choice(range(self.new_population.shape[1]))
                  new_offspring[children,:pivotPoint] = parents[p1,:pivotPoint] 
                  new_offspring[children,pivotPoint:] = parents[p2,pivotPoint:] 
                break
        return new_offspring
            
    def crossoverHandler(self, choice, parents,OFFSPRING_NUM):
        if choice == "uniform":
          return self.uniformCrossover(parents,OFFSPRING_NUM)
        elif choice == "singlepoint":
          return self.singlePointCrossover(parents,OFFSPRING_NUM)

    def mutation(self,offspring_crossover):
  
        size_x = offspring_crossover.shape[0]
        size_y = offspring_crossover.shape[1]

        for idx in range(size_x):

            for _ in range(self.MUTATION_RATE):

                random_weight_index = random.randrange(size_y) # Returns between 0 and size_y-1

                ndaRandom_weight          =           np.random.choice\
                            (np.arange(-1,1,step = 0.001),
                                            size = (1), 
                                         replace = False)

                offspring_crossover[idx,random_weight_index] += ndaRandom_weight

        return offspring_crossover


    def statisticsFileHandler(self):
        from datetime import datetime,date
        current_time = datetime.now().strftime("%H:%M:%S")
        today_date = date.today()
        
        arqFileName = "Gen test - " + str(today_date) + " - " + str(current_time) + ".csv"
        arqFileNameInfo = "Gen test - " + str(today_date) + " - " + str(current_time) + " - info.txt"
        
      
        genInfo = "Generations: %d\nSizes: %s\nOffspring Count: %d\nNumber of Parents: %d\nMutation rate: %d\n"%(self.GENERATIONS,str(self.SIZES),self.OFFSPRING_NUM,self.NUM_PARENTS,self.MUTATION_RATE)
        print(genInfo)
  
        arq = open("GenTests/" + arqFileNameInfo, "w")
        arq.write(genInfo)
        arq.close()
        self.arq = open("GenTests/" + arqFileName,"w")
        self.arq.write("Generation, Best body lengths, Average body length\n")

    def main(self):
        self.statisticsFileHandler()

        for self.generation in range(self.GENERATIONS+1):

            if self.generation >= self.VIEW_GENERATIONS:
              if self.generation % self.VIEW_GENERATIONS == 0:
                self.DRAW = True
                self.TICK = self.TICK_COPY
              else:
                self.DRAW = False
                self.TICK = None
            else:
              self.DRAW = False
              self.TICK = None

            ndaScores,ndaBody_lengths = self.runCurrentGeneration(self.new_population)

            maximum_score,ndaMaximum_bodies,bestAncestorsIndexes = self.getMaximums(ndaScores,ndaBody_lengths)

            if self.generation == self.GENERATIONS+1: # Exit loop without generating new offspring
                break

            print("--------------------------------------")
            print("Cluster: ", self.ID)
            print("Generation:",self.generation)
            #print("Bests scores of generation:",maximum_score)
            print("Best body_length of generation",ndaMaximum_bodies)
            print("Mean body_length of generation",ndaBody_lengths.mean())
            print("-------------------------------------")
            csvLine = "%d, %d, %f\n"%(self.generation,ndaMaximum_bodies.max(),ndaBody_lengths.mean())
            self.arq.write(csvLine)

            # Generate new offspring
            ndaBestParents = self.copyParents(bestAncestorsIndexes)
            OFFSPRING_NUM_MINUS_PARENTS = self.OFFSPRING_NUM - ndaBestParents.shape[0] #Gotta preserve the parents
            crossedNewOffspring = self.crossoverHandler(self.CROSSOVER_ALGORITHM,ndaBestParents,OFFSPRING_NUM_MINUS_PARENTS)
            mutatedNewOffspring = self.mutation(crossedNewOffspring)

            # Preserve the parents
            self.new_population[0:ndaBestParents.shape[0], :] = ndaBestParents
            self.new_population[ndaBestParents.shape[0]:,:] = mutatedNewOffspring
  
        self.returnOverallBest(bestAncestorsIndexes)
        self.arq.close()

        

    def returnOverallBest(self,bestIndexes):
        best = []
        for i in bestIndexes:
            best.append(self.new_population[i])
        print("Saving Weights")
        np.save('best weights.npy',best)





