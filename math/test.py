#%%
import matplotlib.pyplot as plt
#首先定义两个函数（正弦&余弦）
import numpy as np

X=np.linspace(-np.pi,np.pi,256,endpoint=True)#-π to+π的256个值
C,S=np.cos(X),np.sin(X)
plt.plot(X,C)
plt.plot(X,S)
#在ipython的交互环境中需要这句话才能显示出来
plt.show()


#%%
X=np.linspace(0,100,100)

Y = 10 * X+ 0.5 * X *(X-1)* 1

Y2 = 10 + (X -1)* 1

plt.plot(X,Y)

plt.plot(X,Y2)
# plt.xlim([0,1000])
# plt.ylim([0,1000])
plt.show() 

#%%
import math
X=np.linspace(0,10,10)

Y = 10 + np.power(4,X-1)

plt.plot(X,Y)
# plt.xlim([0,1000])
# plt.ylim([0,1000])
plt.show() 


#%%
