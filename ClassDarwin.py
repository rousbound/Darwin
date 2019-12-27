from Cobra import *
import random
import pygame as pg

class Darwin():
    def __init__(self):
        pg.init()
        self.offspring_n = 2000
        self.generations = 50
        self.generation = 0
        self.sizes = [8,9,15,3]
        self.n_parents = 12
        self.mutation_rate = 25

        sizes = self.sizes
        self.n_x = sizes[0]
        self.n_h = []
        for i,n_h in enumerate(sizes[1:-1]):
            self.n_h.append(n_h)
        self.n_y = sizes[-1]
        self.total_weights = self.get_total_weights()
        self.pop_size = (self.offspring_n,self.total_weights)
        self.new_population = np.random.choice(np.arange(-1,1,step=0.01),size = self.pop_size,replace = True)
        self.tick = None #10000
        self.delay = None #1 
        self.draw = False

    def get_total_weights(self):
        sizes = self.sizes
        self.shapes = [[x,y] for (x,y) in zip(sizes[1:],sizes[:-1])]
        self.mult = [[x*y] for (x,y) in zip(sizes[1:],sizes[:-1])]
        self.total = 0
        for i in self.mult:
            self.total += i[0]
        return self.total

    def create(self,population):
        scores = np.empty(self.offspring_n)
        bodys = np.empty(self.offspring_n)
        for i,weight in enumerate(self.new_population):
            game = Game(self.sizes,weights = weight,tick = self.tick,draw= self.draw,delay = self.delay)#,draw= True,tick = 50)
            score,body = game.main()
            scores[i] = score
            bodys[i] = body
        return scores, bodys

    def find_maximum(self,score,body):
        scores = score.copy()
        body= body.copy()
        population_finder = []
        maximum = np.zeros(self.n_parents)
        maximum_body = np.zeros(self.n_parents)
        for index in range(self.n_parents):
            max = np.max(scores)
            max2 = np.max(body)

            idx = np.argmax(scores)
            idx2 = np.argmax(body)

            scores[idx] = 0
            body[idx] = -99999

            maximum[index] = max
            maximum_body[index] = max2

            population_finder.append(idx2)
        return maximum, maximum_body,population_finder

    def create_parents(self,maximum_games,index):
        parents = np.empty((self.n_parents,self.new_population.shape[1]))
        for i,parent in enumerate(parents):
            parents[i] = self.new_population[index[i]]
        return parents

    def cross(self,parents,offspring_n):
        new_offspring = np.empty((offspring_n,parents.shape[1]))
        for k in range(offspring_n):
            while True:
                p1 = random.randint(0,parents.shape[0] -1)
                p2 = random.randint(0,parents.shape[0] -1)
                if p1 != p2:
                    for j in range(self.new_population.shape[1]):
                        if random.uniform(0,1) < 0.5:
                            new_offspring[k,j] = parents[p1,j]
                        else:
                            new_offspring[k,j] = parents[p2,j]
                    break
        return new_offspring

    def mutation(self,offspring_crossover,mutation_rate):
        for idx in range(offspring_crossover.shape[0]):
            for _ in range(mutation_rate):
                i = random.randint(0,offspring_crossover.shape[1] -1)
                random_weight = np.random.choice(np.arange(-1,1,step=0.001),size=(1),replace=False)
                offspring_crossover[idx,i] = offspring_crossover[idx,i] + random_weight
        return offspring_crossover

    def main(self):
        for self.generation in range(self.generations+1):
            self.controls()
            scores,body_lenght = self.create(self.new_population)

            maximum,maximum_body,index_list = self.find_maximum(scores,body_lenght)
            if self.generation == self.generations+1:
                break
            print("generation:",self.generation)
            print("bests scores of generation:",maximum)
            print("best body_lenght of generation",maximum_body)

            parents = self.create_parents(maximum,index_list)

            new_offspring = self.cross(parents,self.offspring_n-parents.shape[0])

            mutated = self.mutation(new_offspring,self.mutation_rate)

            self.new_population[0:parents.shape[0], :] = parents
            self.new_population[parents.shape[0]:,:] = mutated
            print(self.new_population.shape[0])
        return (maximum,maximum_body,index_list)

    def find_best(self,main_outcomes):
        maximum = main_outcomes[0]
        maximum_body = main_outcomes[1]
        index_list = main_outcomes[2]
        best = []
        for i in index_list:
            best.append(self.new_population[i])
        np.save('best weights.npy',best)


    def controls(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[pg.K_d]:
                    if self.draw == False:
                        self.draw = True
                    elif self.draw == True:
                        self.draw = False



darwin = Darwin()
darwin.find_best(darwin.main())
