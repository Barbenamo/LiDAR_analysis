import glob
import os
import pandas as pd
from decodeLidarFile_python import run
import concurrent.futures as cf
import os
# from alternate_filter import filter_points
import multiprocessing as mp
from sort_time_lidar_id import sort_directory
from filter_sort_points import filter_points_v3

def decode_sim_results(directory: str):
    for file in glob.glob(f'{directory}/*/*'):
        run(file)
    pool = cf.ThreadPoolExecutor()
    path_list = [path for path in glob.glob(f'{directory}/*/*/*') if not path.endswith(".csv")]
    velodyne_folders = list(set([os.path.dirname(folder) for folder in path_list]))
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(_filter, velodyne_folders)

def filter_results(directory: str):
    path_list = [path for path in glob.glob(f'{directory}/*/velodyne32e_21700001/*')]
    velodyne_folders = list(set([os.path.dirname(folder) for folder in path_list]))
    print(velodyne_folders)
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(_filter, velodyne_folders)

def _filter(folder: str):
    new_dir = os.path.join(os.path.dirname(folder), 'filtered')
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    filter_points_v3(folder, new_dir)

def renamer(directory: str, run_id_file: str):
    dir_list = [path for path in glob.glob(f'{directory}/*')]
    df = pd.read_csv(run_id_file)
    for folder in dir_list:
        dir, run_id = os.path.split(folder)
        index = df.index[df['1'] == run_id][0] 
        name = df['0'].loc[index]
        os.rename(os.path.join(dir,run_id),os.path.join(dir,name[:20]))

def count_files(directory) ->int:
    files = sum(len(files) for _, _, files in os.walk(f'{directory}'))
    # print(files)
    return files

def sort_time_id(directory):
    dir_list = [path for path in glob.glob(f'{directory}/*')]
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(_sort,dir_list)

def _sort(folder: str):
    dir_to_sort = os.path.join(folder,'filtered')
    print(f'sorting: {dir_to_sort}')    
    destination = os.path.join(folder,'filtered_sorted')
    if not os.path.exists(destination):
        os.makedirs(destination)
    sort_directory(dir_to_sort,destination)



if __name__ == '__main__':
    path = "/home/simteamq/Desktop/lidar-analysis"
    directory = f'{path}/100_run_data_PointCloud_Y3'
    renamer(directory,f'{path}/run_ids/run_id_list_PointCloudY.csv')
    decode_sim_results(directory)
    filter_results(directory)
    sort_time_id(directory) 


    # dir_list = [path for path in glob.glob(f'{directory}/*')]
    # file_list = [file_name.split("/")[-1] for file_name in dir_list]
    # for i in range(len(dir_list)):
    #     os.rename(dir_list[i], f"{file_list[i][:11]}_{file_list[i][11:]}")
        
