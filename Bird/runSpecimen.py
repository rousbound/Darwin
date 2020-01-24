from settings import *
from flappyBird import Game
import numpy as np
import sys

speed = input("Input speed:")
best = np.load(sys.argv[1])
print("saving out:",best)
print(best.shape)
for n,i in enumerate(best):
    print("specimen %d"%n)
    g = Game(sizes = [13,12,21,4],weightsIn=i,gameArgs={'fps' : int(speed)})
    print(g.main())
