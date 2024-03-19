import pathlib
import time
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
from sort_time_lidar_id import sort_directory


def vector_size(x, y, z):
    return np.sqrt(np.power(x, 2) + np.power(y, 2) + np.power(z, 2))


# open directory, read all raw data into pd
# outputDict organization: [output# : [(index,x,y,z,theta,phi,identifier)]] 

def filter_points(directory, output_dir):
    st = time.time()
    outputDict = {}
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        df = pd.read_csv(f)
        df = df.drop(df.columns[0], axis=1)
        x = df['x']
        y = df['y']
        z = df['z']
        id = df['part_id']
        print(f'Working on: {directory}')
        # print(df)
        for i in range(0, len(df.values)):
            distance_from_Lidar = vector_size(x.loc[i], y.loc[i], z.loc[i])
            if id.loc[i] != 53 and id.loc[i] != 0:  # filter by obj id
                df = df.drop([i, i])
                continue
            if distance_from_Lidar >= 2.5:
                df = df.drop([i, i])
                continue  # stop for this iter , and go over to the next iter
        
        df.to_csv(f'{output_dir}/{filename}')
        print(time.time()-st)

def filter_points_v2(directory, output_dir):
    st = time.time()
    print(f'Working on: {directory}')
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        df = pd.read_csv(f)
        outputDataFrame = pd.DataFrame(columns=df.columns)
        outputDataFrame = outputDataFrame.drop(outputDataFrame.columns[0], axis=1)
        x = df['x']
        y = df['y']
        z = df['z']
        id = df['part_id']
        # print(df)
        for i in range(0, len(df.values)):
            distance_from_Lidar = vector_size(x.loc[i], y.loc[i], z.loc[i])
            if id.loc[i] != 53 and id.loc[i] != 0:  # filter by obj id
                continue
            if distance_from_Lidar >= 2.5:
                continue  # stop for this iter , and go over to the next iter
            outputDataFrame.loc[i] = df.loc[i]
        outputDataFrame.to_csv(f'{output_dir}/{filename}')
        print(time.time()-st)

def filter_points_v3(directory, output_dir):
    st = time.time()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        df = pd.read_csv(f)

        # Calculate distance and add it as a new column
        df['distance_from_Lidar'] = vector_size(df['x'], df['y'], df['z'])

        # Filter the DataFrame
        filtered_df = df[(df['part_id'].isin([53, 0])) & (df['distance_from_Lidar'] < 2.5)]

        # Drop the distance column if not needed
        filtered_df = filtered_df.drop(columns=['distance_from_Lidar'])

        # Save the filtered DataFrame to a new CSV file
        output_filename = os.path.join(output_dir, filename)
        filtered_df.to_csv(output_filename, index=False)
    print(f'{directory} took {time.time()-st} [sec]')

# path = "/home/simteamq/Desktop/lidar-analysis/test2"
# filter_points_v3(path,path)
# # filter_points(path,path)