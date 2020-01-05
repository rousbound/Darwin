from Cobra import *
import sys


speed = input("Input speed:")
best = np.load(sys.argv[1])
print("saving out:",best)
print(best.shape)
for n,i in enumerate(best):
    print("specimen %d"%n)
    g = Game([9,9,15,4],weights=i,tick=int(speed),draw=True)
    print(g.main())
