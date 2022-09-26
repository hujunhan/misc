from datetime import date
from importlib.metadata import distribution
import numpy as np
from scipy import stats

likert=[1,2,3,4,5]
np.random.seed(6)
p1=[0.14,0.32,0.29,0.16]
p1.append(1-sum(p1))
data1=np.random.choice(likert,200,p=p1)
print(p1)
np.savetxt('cwy/data1.txt',data1)
np.random.seed(7)
p2=[0.09,0.1,0.14,0.41]
p2.append(1-sum(p2))
print(p2)
data2=np.random.choice(likert,200,p=p2)
t,p=stats.ttest_ind(data1,data2)
print(t,p)
np.savetxt('cwy/data2.txt',data2)
np.random.seed(8)
p2=[0.1,0.15,0.24,0.37]
p2.append(1-sum(p2))
print(p2)
data2=np.random.choice(likert,200,p=p2)
t,p=stats.ttest_ind(data1,data2)
print(t,p)
np.savetxt('cwy/data3.txt',data2)
np.random.seed(9)
p2=[0.05,0.13,0.25,0.29]
p2.append(1-sum(p2))
print(p2)
data2=np.random.choice(likert,200,p=p2)
t,p=stats.ttest_ind(data1,data2)
print(t,p)
np.savetxt('cwy/data4.txt',data2)
