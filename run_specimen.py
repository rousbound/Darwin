from Cobra import *



best = np.load('best weights.npy')
print("saving out:",best)
print(best.shape)
for n,i in enumerate(best):
    print("specimen %d"%n)
    g = Game([8,9,15,4],weights=i,tick=50,draw=True)
    g.main()
