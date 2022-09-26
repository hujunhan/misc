from datetime import date
from importlib.metadata import distribution
import numpy as np

likert=[1,2,3,4,5]
np.random.seed(4)
p=[0.08,0.09,0.04,0.35]
p.append(1-sum(p))
print(p)
data=np.random.choice(likert,200,p=p)
for i in data:
    print(i)