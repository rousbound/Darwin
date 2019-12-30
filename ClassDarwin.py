from Cobra import *
import random
import pygame as pg
import threading

class Darwin():
    def __init__(self):
        pg.init()                  # Standard Build:
        self.OFFSPRING_NUM = 2000 #    2000
        self.GENERATIONS = 200 
        self.VIEW_GENERATIONS = 50
        self.GENERATION = 0
        self.SIZES = [8,9,15,3]    #   [8,9,15,3]
        self.NUM_PARENTS = 1000      #      12
        self.MUTATION_RATE = 25   #      25

        self.TICK_COPY = 1000
        self.TICK = None
        self.DELAY = None 
        self.DRAW = False

        self.lInput = self.SIZES[0]
        self.lHidden = []
        self.lOutput = self.SIZES[-1]
  
        for i,lHidden in enumerate(self.SIZES[1:-1]):
            self.lHidden.append(lHidden)

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
        print("DRAW INSIDE: ", self.DRAW)
        

        for i,weight in enumerate(self.new_population):

            snakeLifeSpan                  =           Game\
                              (self.SIZES,
                                   weights = weight, 
                                      tick = self.TICK, 
                                      draw = self.DRAW, 
                                     delay = self.DELAY)

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

    def cross(self,parents,OFFSPRING_NUM):
        new_offspring = np.empty((OFFSPRING_NUM,parents.shape[1]))

        for k in range(OFFSPRING_NUM):
            while True:
                p1 = random.randrange(parents.shape[0])
                p2 = random.randrange(parents.shape[0])
                if p1 != p2:
                    for j in range(self.new_population.shape[1]):
                        if random.uniform(0,1) < 0.5:
                            new_offspring[k,j] = parents[p1,j]
                        else:
                            new_offspring[k,j] = parents[p2,j]
                    break
        return new_offspring

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

    def main(self):

        for self.GENERATION in range(self.GENERATIONS+1):

            if self.GENERATION >= self.VIEW_GENERATIONS:
              if self.GENERATION % self.VIEW_GENERATIONS == 0:
                self.DRAW = True
                self.TICK = self.TICK_COPY
              else:
                self.DRAW = False
                self.TICK = None
            print("DRAW: ",self.DRAW)

            ndaScores,ndaBody_lengths = self.runCurrentGeneration(self.new_population)

            maximum_score,maximum_bodies,bestAncestorsIndexes = self.getMaximums(ndaScores,ndaBody_lengths)

            if self.GENERATION == self.GENERATIONS+1: # Exit loop without generating new offspring
                break

            print("--------------------------------------")
            print("Generation:",self.GENERATION)
            print("Bests scores of generation:",maximum_score)
            print("Best body_length of generation",maximum_bodies)
            print("Mean body_length of generation",ndaBody_lengths.mean())
            print("-------------------------------------")

            ndaBestParents = self.copyParents(bestAncestorsIndexes)

            OFFSPRING_NUM_MINUS_PARENTS = self.OFFSPRING_NUM - ndaBestParents.shape[0] #Gotta preserve the parents
            
            crossedNewOffspring = self.cross(ndaBestParents,OFFSPRING_NUM_MINUS_PARENTS)

            mutatedNewOffspring = self.mutation(crossedNewOffspring)

            # First NUM_PARENTS indexes are parents, rest are the mutated and crossed NewOffspring
            self.new_population[0:ndaBestParents.shape[0], :] = ndaBestParents
            self.new_population[ndaBestParents.shape[0]:,:] = mutatedNewOffspring
  
        self.returnOverallBest(bestAncestorsIndexes)

        

    def returnOverallBest(self,bestIndexes):
        best = []
        for i in bestIndexes:
            best.append(self.new_population[i])
        print("Saving Weights")
        np.save('best weights.npy',best)





darwin = Darwin()
darwin.main()
