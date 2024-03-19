#
# Download Utilities for simulation data
#
# Copyright Cognata Ltd. (c) 2020 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# All trade-marks, trade names, service marks and logos referenced herein belong to their respective companies
# Proprietary and confidential
from cognata_sim_generator import get_api
import os
import shutil
import tarfile
import zipfile
import glob
import time
from datetime import datetime
import concurrent.futures
from typing import *
from pathlib import Path
from numba import jit
import pandas as pd


def extract_subdir_list(path: str):
    return glob.glob(path + '/*/')

def del_create_dir(dir: str):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

def del_dir(dir: str):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def untar(fname: str):
    if fname.endswith("tar"):
        tar = tarfile.open(fname)
        tar.extractall(os.path.dirname(fname))
        tar.close()
        print
        "Extracted in Current Directory"
    elif fname.endswith("zip"):
        zip_ref = zipfile.ZipFile(fname, 'r')
        zip_ref.extractall(os.path.dirname(fname))
        zip_ref.close()

def extract_tar_zip_dir(root: str):
    file_list = os.listdir(root)
    for f_name in file_list:
        if  ("tar" in f_name) or ("zip" in f_name):
            untar(root + '/' + f_name)
            os.remove(root + '/' + f_name)


def download_data(sim_api: object, simulation_run_id: List[str], download_dir: str, extract_data: bool=True) -> List[str]:
    """
    download data files from simulation servers
    :param sim_api: Cognata API instance
    :param simulation_run_id: string - id of the simulation run
    :param download_dir: string - path to the download directory
    :return:
    string - path to the downloaded dir
    """
    # **** Download data
    sim_data = sim_api.get_simulation_run_files_list(simulation_run_id)

    if sim_data == None or len(sim_data) == 0:
        print(('simulation run-id : ', simulation_run_id, ' is empty.'))
        return False

    # create dir of sim_run_id
    sim_run_id_dir = os.path.join(download_dir, simulation_run_id)
    del_create_dir(sim_run_id_dir)
    download_links = []

    for sensor_data in sim_data:
        if sensor_data['group_type'] == 'system':  # This is the config files.
            for data in sensor_data['files']:
                if data['file_type'] == 'zip' or data['file_type'] == 'json' or data[
                    'file_type'] == 'csv':
                    download_link = sim_api.download_simulation_run_file(simulation_run_id=simulation_run_id,
                                                                         file_name=data['file_name'],
                                                                         allow_redirects=False)
                    download_links.append([data['file_name'], download_link])
        else:
            for data in sensor_data['files']:
                download_link = sim_api.download_simulation_run_file(simulation_run_id=simulation_run_id,
                                                                     file_name=data['file_name'],
                                                                     allow_redirects=False)
                download_links.append([data['file_name'], download_link])

    for filename, download_link in download_links:
        command_line = 'aria2c -x15 -s15 "' + download_link + '" --dir ' + sim_run_id_dir + ' -o ' + filename
        os.system(command_line)

    # Untar / Unzip files
    if extract_data:
        extract_tar_zip_dir(sim_run_id_dir)

    return sim_run_id_dir

def download_simruns(sim_api: object, sim_run_id_list: List[str], download_dir: str, 
                    extract_data: bool=True) -> List[str]:
    # Download Data
    del_aborted_list = []
    for run_id_index, new_simulation_run_id in enumerate(sim_run_id_list):
        sim_run_end_status = sim_api.wait_for_simulation_to_finish(new_simulation_run_id)
        print((datetime.fromtimestamp(time.time()), "simulation run", new_simulation_run_id, "finished with status",
               sim_run_end_status))

        #Remove aborted runs
        if sim_run_end_status == 'aborted':
            del_aborted_list.append(run_id_index)
            continue

        # ** Download data
        sim_download_dir = download_data(sim_api=sim_api, simulation_run_id=new_simulation_run_id,
                                         download_dir=download_dir, extract_data=extract_data)

        if not sim_download_dir:
            print((new_simulation_run_id, ' : fail for some reason.'))
            continue

    # remove aborted runs
    sim_run_id_list = [sim_run_id_list[i] for i in range(len(sim_run_id_list)) if i not in del_aborted_list]
    return sim_run_id_list


def download_data_by_filenames(sim_api: object, simulation_run_id_list: List[str], 
                                download_dir: str, extract_data: bool=True,
                                filenames_to_include: List[str]=['velodyne32e_21700001.zip']) -> List[str]:
    """
    download data files from simulation servers
    :param sim_api: Cognata API instance
    :param simulation_run_id: string - id of the simulation run
    :param download_dir: string - path to the download directory
    :return:
    string - path to the downloaded dir
    """
    # **** Download data
    sim_run_id_dir_list = []
    for simulation_run_id in simulation_run_id_list:
        sim_data = sim_api.get_simulation_run_files_list(simulation_run_id)
        if sim_data == None or len(sim_data) == 0:
            print(('Simulation RunID : ', simulation_run_id, ' is empty.'))  #<---------
            return False

        # create dir of sim_run_id
        sim_run_id_dir = os.path.join(download_dir, simulation_run_id)
        sim_run_id_dir_list.append(sim_run_id_dir)
        del_create_dir(sim_run_id_dir)
        download_links = []
        for sensor_data in sim_data:
            print(sensor_data)
            if sensor_data['group_type'] == 'lidar':  # This is the config files.
                for data in sensor_data['files']:
                    if data['file_name'] in filenames_to_include:
                        download_link = sim_api.download_simulation_run_file(simulation_run_id=simulation_run_id,
                                                                             file_name=data['file_name'],
                                                                             allow_redirects=False)
                        download_links.append([data['file_name'], download_link])
        executor = concurrent.futures.ThreadPoolExecutor()
        pool = []
        for filename, download_link in download_links:
            # if filenames_to_include is None or filename in filenames_to_include:
                pool.append(executor.submit(download_with_aria2, download_link, filename, sim_run_id_dir))
                #command_line = 'aria2c -x15 -s15 "' + download_link + '" --dir ' + sim_run_id_dir + ' -o ' + filename
                #os.system(command_line)
        futures_running = count_futures_running(pool)
        total_futures = len(download_links)
        #while futures_running > total_futures:
        #    print(f"{futures_running}/{total_futures} left")
        #    futures_running = count_futures_running(pool)
        #    time.sleep(0.1)
        executor.shutdown(wait=True)

        # Untar / Unzip files
        if extract_data:
            extract_tar_zip_dir(sim_run_id_dir)

    return pool

def count_futures_running(futures: List[concurrent.futures.ThreadPoolExecutor]) -> int:
    """Checking number of running futures in a given pool. Should send a copy of the pool

    ### Parameters
    1. futures : List[ThreadPoolExecutor]
        - The pool of sent futures

    ### Returns
    - int
        - Number of futures that are still running
    """
    count = 0
    for future in futures:
        if not future.done():
            count += 1
        else:
            futures.remove(future)
    return count

def download_with_aria2(url: str, filename: str, download_dir: Optional[str]=None) -> None:
    """Using wget through aria2 to download a file

    Args:
        url (str): the URL for the given file to download
        filename (str): chosen file name for downloaded file
        dir (str, optional): directory for saving the file.
            Defaults to None, in which case the file will be downloaded to the user's download folder.
    """
    if download_dir is None:
        download_dir = str(Path.home() / "Downloads")
    command_line = f'aria2c -x 16 -s 100 "{url}" --dir {download_dir} -o {filename} --show-console-readout=false --download-result=hide'
    os.system(command_line)

path = '/home/simteamq/Desktop/lidar-analysis'
api = get_api()
df = pd.read_csv('run_ids/run_id_list_PointCloudY.csv')
run_id_list = df['1']
print(run_id_list)
for i in range(len(run_id_list)):
    download_data_by_filenames(api,[run_id_list.loc[i]], f'{path}/100_run_data_PointCloud_Y3', True)

