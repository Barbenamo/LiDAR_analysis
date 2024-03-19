import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import scipy
from scipy.optimize import curve_fit
import statistics
import math

# returns the 32 ray theta angles in randians
def get_theta_segment(df):
    return df['theta'][:32]

def get_phi_segment(df):
    return sorted(set(df['phi']))
# radians
def calc_phi_from_y(x,y):
    return math.atan2(y,x)



if __name__ == '__main__':
    path = '/home/simteamq/Desktop/lidar-analysis'
    df_sp = pd.read_csv(f'{path}/scanning_pattern_phi_test_.csv')
    theta_angles = get_theta_segment(df_sp)
    phi_angles = get_phi_segment(df_sp)
    # print(len(phi_angles))
    df_sim = pd.read_csv(f'{path}/nn_run_include_normal.csv')
    delta_angles = []
    x, y, z = df_sim['x'], df_sim['y'], df_sim['z']
    for i in range(len(df_sim)):
        x_i = x.loc[i]
        y_i = y.loc[i]
        print(calc_phi_from_y(x_i,y_i)*180/math.pi, phi_angles[i%303]*180/math.pi)
        delta_angles.append(abs(calc_phi_from_y(x_i,y_i)*180/math.pi-phi_angles[i%303]*180/math.pi))
    print(delta_angles)