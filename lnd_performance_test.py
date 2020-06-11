#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Time consuming
y_list = [4.593326,3.926037,4.063145,4.178354,4.01259]
y_list = y_list+ [3.795474,4.078779,4.264592,4.073657,4.262957]
y_list = y_list+ [5.067245,5.067862,5.377964,5.202581,6.281425]
y_list = y_list+ [6.435726,6.314366,6.270448,6.17416,6.173198]
y_list = y_list+ [7.14413,7.208339,7.317925,7.814415,7.522867]
y_list = y_list+ [9.348118,9.73535,9.72385,10.011137,9.521669]
y_list = y_list+ [11.878434,13.878347,18.543237,14.589488,13.774271]

# number of batches
x_list = [1 for i in range(5)]
x_list = x_list+ [2 for i in range(5)]
x_list = x_list+ [10 for i in range(5)]
x_list = x_list+ [20 for i in range(5)]
x_list = x_list+ [30 for i in range(5)]
x_list = x_list+ [40 for i in range(5)]
x_list = x_list+ [50 for i in range(5)]

y =np.array(y_list) 
x = np.array(x_list).reshape(-1, 1) 

# create a linear regression model
model = LinearRegression()
model.fit(x, y)

# predict y from the data
x_new = np.linspace(0, 50, 10)
y_new = model.predict(x_new[:, np.newaxis])

# plot the results
plt.figure(figsize=(6, 4))
ax = plt.axes()
ax.scatter(x, y)
ax.plot(x_new, y_new)

ax.set_xlabel('Number')
ax.set_ylabel('Time')

ax.axis('tight')

plt.savefig('lnd.png')
# plt.show()

print(f"R-square = {model.score(x, y)}") # R^2
print(f"Slope = {model.coef_[0]}") # slope
print(f"Intercept = {model.intercept_}") # intercept
print(f"For every incrementing second, the lnd can process roughly {round(20/model.coef_[0],0)} transactions")

