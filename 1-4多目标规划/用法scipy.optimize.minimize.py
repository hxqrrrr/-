from scipy.optimize import minimize
import numpy as np

fun = lambda x: x+1/x
x0 = np.array([2]) # 初始值
res = minimize(fun, x0, method='BFGS')
print(res.fun) # 初始值为2时，输出结果为 1.0 

#对比

from scipy.optimize import minimize
import numpy as np

fun = lambda x: x+1/x
x0 = np.array([5]) # 初始值为5
res = minimize(fun, x0, method='BFGS')
print(res.fun) # 初始值为2时，输出结果为 -7355.299807411861

# 结果不同，说明在该方法下，初始值对结果的影响很大。
#多元条件约束优化
from scipy.optimize import minimize
import numpy as np

fun = lambda x: (2+x[0])/(1+x[1])-3*x[0]+4*x[2]
x0 = np.array([0.5,0.5,0.5])

cons = [{'type':'ineq', 'fun':lambda x:x[0]-0.1},
        {'type':'ineq', 'fun':lambda x:-x[0]+0.9},
        {'type':'ineq', 'fun':lambda x:x[1]-0.1},
        {'type':'ineq', 'fun':lambda x:-x[1]+0.9},
        {'type':'ineq', 'fun':lambda x:x[2]-0.1},
        {'type':'ineq', 'fun':lambda x:-x[2]+0.9}]

res = minimize(fun, x0, method='SLSQP', constraints=cons)
print(res.fun) # -0.773684210526435
print(res.x) # [0.9 0.9 0.1]


#
from scipy.optimize import minimize
import numpy as np

fun = lambda x: np.log2(1+x[0]*2/3)+np.log2(1+x[1]*3/4)
x0 = np.array([0.5,0.5])

cons = [{'type':'ineq', 'fun':lambda x:np.log2(1+x[0]*2/5)-5},
        {'type':'ineq', 'fun':lambda x:np.log2(1+x[1]*3/2)-5}]

res = minimize(fun, x0, method='SLSQP', constraints=cons)
print(res.fun) # 9.763212360886708
print(res.x) # [77.5        20.66666658]

##题目均来自https://0809zheng.github.io/2021/08/23/minimize.html