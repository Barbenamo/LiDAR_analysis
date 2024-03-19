import pandas as pd
import math


# Coded by Bar Ben Amo

def convert_coordinate_system(dir):
    dir = dir  # '/home/simteamq/Desktop/project_git/Bar/'
    f = f'{dir}/scanningPattern_velodyne32e2108.csv'
    df = pd.read_csv(f)
    x = [0] * len(df.values)
    y = [0] * len(df.values)
    z = [0] * len(df.values)
    R = 0.532 #0.866
    for i in range(len(df)):
        theta = df['theta'].loc[i] * math.pi / 180
        phi = df['phi'].loc[i] * math.pi / 180
        x[i] = R
        y[i] = R * math.tan(phi)
        z[i] = R * math.tan(theta) / math.cos(phi)
    df['x'] = x
    df['y'] = y
    df['z'] = z
    df.to_csv(f'{dir}/full_scanning_pattern_new_sim.csv')
    return df

path = '/home/simteamq/Desktop/lidar-analysis'
convert_coordinate_system(path)