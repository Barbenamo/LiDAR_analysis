import pathlib
import statistics
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
import json
# Coded and edited by Bar Ben Amo and Jacob


path = '/home/simteamq/Desktop/lidar-analysis'
f = f'{path}/scanningPattern_velodyne32e2108.csv'
df = pd.read_csv(f)
R = 0.532
theta = df['theta'] * math.pi / 180
phi = df['phi']* math.pi / 180
print(theta)
df['theta'] = theta
df['phi'] = phi
identifier = df['identifier']
x = [0] * len(df.values)
y = [0] * len(df.values)
z = [0] * len(df.values)
phi_edge = 25.0639611 * math.pi / 180
for i in range(0,len(df.values)):
    x[i] =R
    y[i] = R * math.tan(phi.loc[i])  #TODO check this conigurations
    z[i] = R * math.tan(theta.loc[i])/math.cos(phi.loc[i])
 
df['x'] = x
df['y'] = y
df['z'] = z
print('im here!')
for i in range(0,len(df.values)):
    if phi.loc[i] > phi_edge and phi.loc[i] < 2*math.pi-phi_edge:
        df = df.drop([i, i])
print(df)
df.to_csv(f'{path}/scanning_pattern_phi_test_.csv')

