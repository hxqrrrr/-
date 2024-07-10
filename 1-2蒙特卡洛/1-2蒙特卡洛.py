#程序不在了，这个不是
import numpy as np
import matplotlib.pylab as plt
x = np.linspace(0,1,num=50)
y = np.log(1 + x) / (1 + x**2)
plt.plot(x,y,'-')