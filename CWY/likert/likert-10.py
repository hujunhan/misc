from datetime import date
from importlib.metadata import distribution
import numpy as np

likert=[1,2,3,4,5]
np.random.seed(5)
p=[0.04,0.05,0.12,0.45]
p.append(1-sum(p))
print(p)
data=np.random.choice(likert,200,p=p)
for i in data:
    print(i)