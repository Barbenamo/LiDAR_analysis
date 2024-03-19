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
import time
from sort_time_lidar_id import sort_directory

def vector_size(x, y, z):
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))

# open directory, read all raw data into pd
# outputDict organization: [output# : [(index,x,y,z,theta,phi,identifier)]] 

def filter_points(directory):
    st = time.time()
    outputDict = {}
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        df = pd.read_csv(f)
        df = df.drop(df.columns[0], axis=1)
        dfc = df[0:0]
        x = df['x']
        y = df['y']
        z = df['z']
        id = df['part_id']
        print(f'Working on: {directory}')
        for i in range(0, len(df.values)):
            distance_from_Lidar = vector_size(x.loc[i], y.loc[i], z.loc[i])
            if id.loc[i] == 0 and distance_from_Lidar <=2.5:  # filter by obj id
                dfc = dfc.append(df.iloc[i])
                continue
        dfc.to_csv(f'{directory}/filtered/{filename}')
        et = time.time()
        print(et-st)

# path = '/home/simteamq/Desktop/lidar-analysis'
# directory = f'{path}/velodyne32e_21700001'
# filter_points(directory)
