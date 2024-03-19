import pandas as pd
import numpy as np
import os
import statistics as st
import glob
#Coded and edited By Bar Ben Amo
#This file contains various methods that generate different dataframe in order to analyze.

# This method go over a directory and a reference to create a difference in coordinates dataframe
def generate_delta_df(directory,reference_file):
    files = glob.glob(f'{directory}/filtered_sorted/*')
    noise = float(os.path.basename(directory).split('_')[-1])
    dfrf = pd.read_csv(reference_file)
    output_df = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file)
        merged_df = df.merge(dfrf, on=['lidar_identifier', 'point_idx'], suffixes=('1', '2'))
        merged_df['del_x'] = merged_df['x1'] - merged_df['x2']
        merged_df['del_y'] = merged_df['y1'] - merged_df['y2']
        merged_df['del_z'] = merged_df['z1'] - merged_df['z2']
        merged_df['noise'] = noise
        differences_df = merged_df[['noise','lidar_identifier', 'point_idx', 'del_x', 'del_y', 'del_z']]
        output_df = pd.concat([output_df,differences_df])
    output_df = output_df.rename(columns={'noise':'noise','lidar_identifier':'lidar_identifier',
                                              'point_idx':'point_idx','del_x':'x', 'del_y':'y', 'del_z':'z'})
    return output_df   

def generate_delta_df_SP_compare(directory,reference_file):
    files = glob.glob(f'{directory}/filtered_sorted/*')
    noise = float(os.path.basename(directory).split('_')[-1])
    dfrf = pd.read_csv(reference_file)
    output_df = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file)
        merged_df = df.merge(dfrf, on=['lidar_identifier','delta_time'], suffixes=('1', '2'))
        merged_df['del_x'] = merged_df['x1'] - merged_df['x2']
        merged_df['del_y'] = merged_df['y1'] - merged_df['y2']
        merged_df['del_z'] = merged_df['z1'] - merged_df['z2']
        merged_df['noise'] = noise
        differences_df = merged_df[['noise','lidar_identifier','delta_time', 'del_x', 'del_y', 'del_z']]
        output_df = pd.concat([output_df,differences_df])
    output_df = output_df.rename(columns={'noise':'noise','lidar_identifier':'lidar_identifier',
                                              'delta_time':'delta_time','del_x':'x', 'del_y':'y', 'del_z':'z'})
    return output_df  

# This method go over a directory and a reference to create a mean of differences in coordinates dataframe
def generate_mean_df(directory, reference_file):
    files = glob.glob(f'{directory}/filtered_sorted/*')
    noise = float(os.path.basename(directory).split('_')[-1])
    dfrf = pd.read_csv(reference_file)
    multi_diff_df = pd.DataFrame()
    diff_df = pd.DataFrame(columns=['x_difference_mean', 'y_difference_mean', 'z_difference_mean', 'noise'])
    for file in files:
        df = pd.read_csv(file)
        merged_df = df.merge(dfrf, on=['lidar_identifier', 'point_idx'], suffixes=('1', '2'))
        diff_df['x_difference_mean'] = merged_df['x1'] - merged_df['x2']
        diff_df['y_difference_mean'] = merged_df['y1'] - merged_df['y2']
        diff_df['z_difference_mean'] = merged_df['z1'] - merged_df['z2']
        diff_df['noise'] = noise
        multi_diff_df = pd.concat([multi_diff_df,diff_df])
    
    final_df = pd.DataFrame()
    final_df['x'] = [np.mean(multi_diff_df['x_difference_mean'])]
    final_df['y'] = [np.mean(multi_diff_df['y_difference_mean'])]
    final_df['z'] = [np.mean(multi_diff_df['z_difference_mean'])]
    final_df['noise'] = [np.mean(multi_diff_df['noise'])]
    return final_df

def generate_mean_df_SP_compare(directory, reference_file):
    files = glob.glob(f'{directory}/filtered_sorted/*')
    noise = float(os.path.basename(directory).split('_')[-1])
    dfrf = pd.read_csv(reference_file)
    multi_diff_df = pd.DataFrame()
    diff_df = pd.DataFrame(columns=['x_difference_mean', 'y_difference_mean', 'z_difference_mean', 'noise'])
    for file in files:
        df = pd.read_csv(file)
        merged_df = df.merge(dfrf, on=['lidar_identifier','delta_time'], suffixes=('1', '2'))
        diff_df['x_difference_mean'] = merged_df['x1'] - merged_df['x2']
        diff_df['y_difference_mean'] = merged_df['y1'] - merged_df['y2']
        diff_df['z_difference_mean'] = merged_df['z1'] - merged_df['z2']
        diff_df['noise'] = noise
        multi_diff_df = pd.concat([multi_diff_df,diff_df])
    
    final_df = pd.DataFrame()
    final_df['x'] = [np.mean(multi_diff_df['x_difference_mean'])]
    final_df['y'] = [np.mean(multi_diff_df['y_difference_mean'])]
    final_df['z'] = [np.mean(multi_diff_df['z_difference_mean'])]
    final_df['noise'] = [np.mean(multi_diff_df['noise'])]
    return final_df

# This method go over a directory and a reference to create a max of difference in coordinates dataframe
def generate_max_delta_df(directory,reference_file):
    files = glob.glob(f'{directory}/filtered_sorted/*')
    noise = float(os.path.basename(directory).split('_')[-1])
    dfrf = pd.read_csv(reference_file)
    output_df = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file)
        merged_df = df.merge(dfrf, on=['lidar_identifier', 'point_idx'], suffixes=('1', '2'))
        merged_df['del_x'] = merged_df['x1'] - merged_df['x2']
        merged_df['del_y'] = merged_df['y1'] - merged_df['y2']
        merged_df['del_z'] = merged_df['z1'] - merged_df['z2']
        merged_df['noise'] = noise
        differences_df = merged_df[['noise','lidar_identifier', 'point_idx', 'del_x', 'del_y', 'del_z']]
        output_df = pd.concat([output_df,differences_df])
    final_df = pd.DataFrame()
    final_df['x'] = [np.max(output_df['del_x'])]
    final_df['y'] = [np.max(output_df['del_y'])]
    final_df['z'] = [np.max(output_df['del_z'])]
    final_df['noise'] = [np.mean(output_df['noise'])]
    return final_df   

def generate_max_delta_df_SP_compare(directory,reference_file):
    files = glob.glob(f'{directory}/filtered_sorted/*')
    noise = float(os.path.basename(directory).split('_')[-1])
    dfrf = pd.read_csv(reference_file)
    output_df = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file)
        merged_df = df.merge(dfrf, on=['lidar_identifier','delta_time'], suffixes=('1', '2'))
        merged_df['del_x'] = merged_df['x1'] - merged_df['x2']
        merged_df['del_y'] = merged_df['y1'] - merged_df['y2']
        merged_df['del_z'] = merged_df['z1'] - merged_df['z2']
        merged_df['noise'] = noise
        differences_df = merged_df[['noise','lidar_identifier','delta_time', 'del_x', 'del_y', 'del_z']]
        output_df = pd.concat([output_df,differences_df])
    final_df = pd.DataFrame()
    final_df['x'] = [np.max(output_df['del_x'])]
    final_df['y'] = [np.max(output_df['del_y'])]
    final_df['z'] = [np.max(output_df['del_z'])]
    final_df['noise'] = [np.mean(output_df['noise'])]
    return final_df  

# this method generate a dataframe out of all subdirectories that contaning various noises.
# type is a string and must be 'delta','mean' or 'max'!
def generate_accumulating_df(directory:str, reference_file:str, type: str):
    sub_dirs = glob.glob(f'{directory}/*')
    final_df = pd.DataFrame()
    for sub_dir in sub_dirs:
        print(f'working on {os.path.split(sub_dir)[-1]}')
        if type == 'max':
            temp_df = generate_max_delta_df_SP_compare(sub_dir,reference_file)
        if type == 'mean':
            temp_df = generate_mean_df_SP_compare(sub_dir,reference_file)
        if type == 'delta':
            temp_df = generate_delta_df_SP_compare(sub_dir,reference_file)
        final_df = pd.concat([final_df,temp_df])
    return final_df.sort_values(by=['noise']) 

if __name__ == '__main__':
    path ='/home/simteamq/Desktop/lidar-analysis'
    reference_file = '/home/simteamq/Desktop/lidar-analysis/references/full_scanning_pattern_new_sim.csv'
    directory =  f'{path}/100_run_data_PointCloud_Y3'
    df1 = generate_accumulating_df(directory,reference_file,'max')
    df1.to_csv(f'{path}/results/max_deltas_100_PCY3.csv')

    df2 = generate_accumulating_df(directory,reference_file,'mean')
    df2.to_csv(f'{path}/results/mean_deltas_100_PCY3.csv')

    df3 = generate_accumulating_df(directory,reference_file,'delta')
    df3.to_csv(f'{path}/results/deltas_100_PCY3.csv')

