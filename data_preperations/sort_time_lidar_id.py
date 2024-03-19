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

# -------------sort a directory of files----------
def sort_directory(directory, destination):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        df = pd.read_csv(f)
        df.sort_values('delta_time', inplace=True)
        time_array = np.array(df["delta_time"])
        unique_array = sorted(list(set(time_array)))
        final_dframe = pd.DataFrame()
        for time in unique_array:
            new_df = df[df["delta_time"] == time].copy()
            new_df.sort_values(by="lidar_identifier",inplace=True)
            final_dframe = pd.concat([final_dframe, new_df], ignore_index=True)
            final_dframe.drop("Unnamed: 0", axis=1, inplace=True)
        final_dframe.to_csv(f"{destination}/{filename}")





# -------------sort single file----------
# delta times is also time and lidar_id is also identifier
def sort_single_file(path):
    df = pd.read_csv(f'{path}/ideal_points_new.csv')
    df.sort_values('time', inplace=True)
    time_array = np.array(df["time"])
    unique_array = sorted(list(set(time_array)))
    final_dframe = pd.DataFrame()
    for time in unique_array:
        new_df = df[df["time"] == time]
        new_df.sort_values(by="lidar id", inplace=True)
        final_dframe = pd.concat([final_dframe, new_df], ignore_index=True)
        final_dframe.drop("Unnamed: 0", axis=1, inplace=True)
    final_dframe.to_csv(f'{path}/ideal_points_new_sorted.csv')


# path = '/home/simteamq/Desktop/lidar-analysis/multiple_run_data/Phi_0.00070/filtered'
# if not os.path.exists(f'{os.path.dirname(path)}/filtered_sorted'):
#     os.makedirs(f'{os.path.dirname(path)}/filtered_sorted')
# sort_directory(path,f'{os.path.dirname(path)}/filtered_sorted')

