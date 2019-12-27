from Cobra import *



best = np.load('best weights.npy')
print(best.shape)
for n,i in enumerate(best):
    print("specimen %d"%n)
    g = Game([8,10,10,4],weights=i,tick=50,draw=True)
    g.main()
