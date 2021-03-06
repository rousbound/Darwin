from datetime import datetime,date
import numpy as np
import random
import pygame as pg


class Evolution():
    def __init__(self,  
                  offspring_num,
                  generations,
                  sizes, 
                  num_parents,
                  mutation_rate,
                  crossing_algorithm,
                  cluster_id = "",
                  saving_csv = False,
                  saving_txt = False,
                  saving_dna = False,
                  saveDnaThreshold = 90,
                  tty = None,
                  loadDnaPath = None,
                  game = None,
                  gameArgs = None):

        self.game = game
        self.gameArgs = gameArgs
        self.TTY = tty 
        self.ID = cluster_id
        self.OFFSPRING_NUM = offspring_num  
        self.GENERATIONS = generations 
        self.generation = 0
        self.SIZES = sizes           
        self.OLD_DNA_PATH = loadDnaPath

        self.NUM_PARENTS = num_parents
        self.MUTATION_RATE = mutation_rate   
        self.CROSSOVER_ALGORITHM = crossing_algorithm


        self.SAVING_CSV = saving_csv
        self.SAVING_TXT = saving_txt
        self.SAVING_DNA = saving_dna
        self.saveDnaThreshold = saveDnaThreshold
        self.dnasSaved = 1

        self.lInput = self.SIZES[0]
        self.lHidden = self.SIZES[1:-1]
        self.lOutput = self.SIZES[-1]
  
        self.total_weights = self.get_total_weights()
        self.population_shape = (self.OFFSPRING_NUM,self.total_weights)

        # Import parents from previously trained offspring
        if self.OLD_DNA_PATH: 
          old_dna = np.load(self.OLD_DNA_PATH)
          self.nda_newPopulation = np.empty(self.population_shape)
          self.nda_newPopulation[0:self.NUM_PARENTS, :] = old_dna

          self.nda_newPopulation[self.NUM_PARENTS:,:] = np.random.choice \
                                (np.arange(-1,1,step = 0.01),
                                                size = (self.OFFSPRING_NUM - \
                                                        self.NUM_PARENTS, \
                                                        self.total_weights),
                                             replace = True)

        # Initiate all the population randomly
        else:
          self.nda_newPopulation             =            np.random.choice \
                                (np.arange(-1,1,step = 0.01),
                                                size = self.population_shape,
                                             replace = True)


    def get_total_weights(self):
        self.mult = [x*y for (x,y) in zip(self.SIZES[1:],self.SIZES[:-1])]
        return sum(self.mult)

    def runCurrentGeneration(self,population):

        fitnesses = np.empty(self.OFFSPRING_NUM)
        scores = np.empty(self.OFFSPRING_NUM)
        

        for i,weight in enumerate(self.nda_newPopulation):

            snakeLifeSpan              =               self.game\
                               (sizes  = self.SIZES,
                               weights = weight,
                               gameArgs = self.gameArgs) 

            fitness, score = snakeLifeSpan.main()
            fitnesses[i] = fitness
            scores[i] = score

        return fitnesses, scores

    def uniformCrossover(self,parents,OFFSPRING_NUM):
        new_offspring = np.empty((OFFSPRING_NUM,parents.shape[1]))

        for children in range(OFFSPRING_NUM):
            while True:
                p1 = random.randrange(parents.shape[0])
                p2 = random.randrange(parents.shape[0])
                if p1 != p2:
                  for weight in range(self.nda_newPopulation.shape[1]):
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
                  pivotPoint = random.choice(range(self.nda_newPopulation.shape[1]))
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

                # Returns between 0 and size_y-1
                random_weight_index = random.randrange(size_y) 
                nda_Random_weight          =           np.random.choice\
                            (np.arange(-1,1,step = 0.001),
                                            size = (1), 
                                         replace = False)

                offspring_crossover[idx,random_weight_index] += nda_Random_weight

        return offspring_crossover


    def statisticsFileHandler(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        today_date = date.today()
        
        self.infoHeader = "Gen test - "      + \
                           str(today_date)   + \
                           " - "             + \
                     str(current_time) + "-" + \
                           str(self.ID)

        
        arqFileName = self.infoHeader + ".csv"
        arqFileNameInfo = self.infoHeader + " - info.txt"
        
      
        genInfo = "Generations: %d\n"        %     self.GENERATIONS     + \
                   "Sizes: %s\n"             %     str(self.SIZES)      + \
                   "Offspring Count: %d\n"   %     self.OFFSPRING_NUM   + \
                   "Number of Parents: %d\n" %     self.NUM_PARENTS     + \
                   "Mutation rate: %d\n"     %      self.MUTATION_RATE 

        print(genInfo)
  
        self.folder = "GenTests/"

        if self.SAVING_TXT:
          arq = open(self.folder + arqFileNameInfo, "w")
          arq.write(genInfo)
          arq.close()

        if self.SAVING_CSV:
          self.arq = open(self.folder + arqFileName, "w")
          self.arq.write("Generation, Best body lengths, Average body length\n")

    def main(self):
        self.statisticsFileHandler()

        for self.generation in range(self.GENERATIONS+1):

            nda_Scores,\
            nda_BodyLengths = self.runCurrentGeneration(self.nda_newPopulation)
            self.nda_bestAncestorsIndexes = np.argsort(-nda_Scores)[:self.NUM_PARENTS]
            nda_MaximumBodies = -np.sort(-nda_BodyLengths)[:self.NUM_PARENTS]
            if self.generation == self.GENERATIONS+1: 
                break
            current_time = datetime.now().strftime("%H:%M:%S")

            statisticsMonitor = "-------------------------------------------------\n"   + \
            "Current Time:%s\n"                     %                 str(current_time) + \
            "Cluster: %s\n"                         %                      str(self.ID) + \
            "Generation: %s\n"                      %              str(self.generation) + \
            "Best body_lengths of generation: %s\n"  %         str(nda_MaximumBodies) + \
            "Mean body_length of generation: %f\n"  %            nda_BodyLengths.mean() + \
            "-----------------------------------------------------------------------\n"

            if self.TTY:
             tty = "/dev/pts/" + str(self.TTY)
             with open(tty, "wb+", buffering=0) as term:
               term.write(statisticsMonitor.encode()) 
            else:
              print(statisticsMonitor)
      
            if self.SAVING_CSV:
              csvLine = "%d, %d, %f\n"      %           (self.generation,\
                                                    nda_MaximumBodies[0],\
                                                    nda_BodyLengths.mean())
              self.arq.write(csvLine)
            if self.saveDnaThreshold:
              if nda_MaximumBodies[0] > self.saveDnaThreshold:
                self.returnOverallBest(nda_MaximumBodies[0])

            # Generate new offspring
            nda_BestParents = np.array([self.nda_newPopulation[x]\
                                 for x in self.nda_bestAncestorsIndexes])

            OFFSPRING_NUM_MINUS_PARENTS = self.OFFSPRING_NUM - self.NUM_PARENTS

            nda_crossedNewOffspring        =            self.crossoverHandler\
                                              (self.CROSSOVER_ALGORITHM, \
                                              nda_BestParents,            \
                                              OFFSPRING_NUM_MINUS_PARENTS)

            nda_mutatedNewOffspring = self.mutation(nda_crossedNewOffspring)

            # Preserve the parents
            self.nda_newPopulation[0:nda_BestParents.shape[0], :] = nda_BestParents
            self.nda_newPopulation[nda_BestParents.shape[0]:,:] = nda_mutatedNewOffspring
  
        if self.SAVING_DNA:
          self.returnOverallBest()
        if self.SAVING_CSV:
          self.arq.close()

        

    def returnOverallBest(self,maximumBody = ""):
        bestIndexes = self.nda_bestAncestorsIndexes
        best = np.zeros((self.NUM_PARENTS,self.total_weights))
        for i,bestIndex in enumerate(bestIndexes):
            best[i] = self.nda_newPopulation[bestIndex]
        print("Saving Weights")
        np.save(self.folder + self.infoHeader + "-" + str(self.dnasSaved) + "-" + str(maximumBody) + '.npy' , best)
        self.dnasSaved += 1





