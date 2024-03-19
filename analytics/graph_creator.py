import pathlib
from sys import displayhook
import pandas as pd
import numpy as np
from numpy.lib import recfunctions
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import math
import os
import statistics
import seaborn as sns
from delta_creator import delta_creator
# Coded and edited by Bar Ben Amo

# -------statistics and plotting - histograma-------#

path = '/home/simteamq/Desktop/lidar-analysis'
df = delta_creator(f'{path}/multiple_run_data/Phi_0.0/filtered_sorted/output9.csv',
                   f'{path}/scanning_pattern_phi_test_.csv')
print(df)

del_x = [0]*len(df)
del_y = [0]*len(df)
del_z = [0]*len(df)

for key in range(len(df)):
    # print(data.get(key))
    del_x[key] = (df['x'].loc[key])
    del_y[key] = (df['y'].loc[key])
    del_z[key] = (df['z'].loc[key])

data = del_x
mean = statistics.mean(data=data)
std_dev = statistics.stdev(data=data)
num_samples = len(data)
print(num_samples)
print(f'mean: {mean}')
print(f'standard deviation:{std_dev}')
print(min(data))
print(max(data))
x_range = np.linspace(min(data),max(data),15)
y_values = [0]*len(x_range) # contains counters that count how many samples fit in the specific area
y_dict = {}
h = x_range[1]-x_range[0]
index = 0
for i in range(0,len(data)):
    index = int((data[i]-x_range[0])/h)
    y_values[int(index)] +=1
    index = f"{index*h}-{index*h+h}"
    if not index in y_dict.keys():
        y_dict[index] = []
    y_dict[index].append(data[i])

# --histograma--
# mean_y = statistics.mean(data)
# std_dev = statistics.pstdev(data)
# plt.hist(data, bins=20, density=True, alpha=0.6, color='b',stacked=True)
# x_range = np.linspace(min(data), max(data), 100)
# y_values = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_range - mean_y) / std_dev)**2)
# 

# plt.plot(x_range, y_values, color='r')

g= sns.barplot(data=df,x = x_range,y = y_values)
plt.grid(True)
xlabels = ['{:,.5f}'.format(x) + ' mm' for x in x_range*1000]
g.set_xticklabels(xlabels)

if data == del_x:
    graph_name = 'x'
elif data == del_y:
    graph_name = 'y'
else:
    graph_name = 'z'
plt.xlabel('Error value')
plt.ylabel('# of occurrences')
plt.title(f'Delta {graph_name}')
plt.show()