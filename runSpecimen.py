from Cobra import *
import sys



best = np.load(sys.argv[2])
print("saving out:",best)
print(best.shape)
for n,i in enumerate(best):
    print("specimen %d"%n)
    g = Game([8,9,15,4],weights=i,tick=int(sys.argv[1]),draw=True)
    print(g.main())
