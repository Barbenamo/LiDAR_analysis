import pathlib
import pandas as pd
import numpy as np
from numpy.lib import recfunctions
# from IPython.core.display import HTML

# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
# from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting 
import math
import os, sys

# ANSI Escape Codes

BLACK = '\033[0;30m'      
RED = '\033[0;31m'
GREEN = '\033[0;32m'
BROWN = '\033[0;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
CYAN = '\033[0;36m'
GRAY = '\033[0;37m'
DARK_GRAY = '\033[1;30m'
LIGHT_RED = '\033[1;31m'
LIGHT_GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
LIGHT_BLUE = '\033[1;34m'
LIGHT_PURPLE = '\033[1;35m'
LIGHT_CYAN = '\033[1;36m'
WHITE = '\033[1;37m'
END = '\033[0m'



def makeAnOutput(directory_name):
    
    try:
        # Check if the directory exists
        if not os.path.exists(directory_name):
            # If the directory does not exist, create it
            os.makedirs(directory_name)
            print(GREEN + f"Directory '{directory_name}' has been created successfully!" + END)
        else:
            print(GREEN + f"{directory_name} is already in the project." + END)
    except:
        print(RED + f"An exception occurred creating {directory_name}" + END)
        
        
        
        
def get_dir_names(dir_path):
  """Gets all directory names within the specified directory path."""
  try:
    dir_list = os.listdir(dir_path)
    dirs = [d for d in dir_list if os.path.isdir(os.path.join(dir_path, d))]
    return dirs
  except FileNotFoundError:
    print(f"Directory '{dir_path}' not found.")
    return []


#----------------------------------------------------------------------------------------------------------# Romano's code above

# def plotting(x,y, z):

#     fig = plt.figure()
#     ax = fig.gca(projection='3d')

#     ax.plot3D(x, y, z, 'green')
#     plt.show()

def size(x,y,z):
    return math.sqrt(x**2+y**2+z**2)

LIDAR_COLUMN_NAMES = ['x', 'y', 'z', 'intensity', 'lidar_identifier', 'delta_time',
                      'Class', 'ID', 'lidar_mat_id', 'normal_cos', 'part_id', 'point_idx',
                      'reference_reflectivity', 'nominator', 'denominator', 'reference_distance',
                      'normal angle theta', 'normal angle phi']

MINUS_FILL = ['Class', 'ID']

ZERO_FILL = ['x', 'y', 'z', 'intensity', 'lidar_identifier', 'delta_time', 'lidar_mat_id', 'normal_cos',
             'part_id', 'point_idx', 'reference_reflectivity', 'nominator', 'denominator', 'reference_distance',
             'normal angle theta', 'normal angle phi']

DROPPED_FIELDS = ['classInstance', 'StructurePointindex', 'fillfactor', 'place holder1',
                  'place holder2', 'place holder3', 'place holder4', 'place holder5', 'place holder6',
                  'place holder7']


def decodeLidarFile(file, withMeta=True):
    """
    Previous signature, kept for backwards compatibility

    :param file: full path to lidar file
    :param withMeta: depricated bool
    :return:
    """
    return decode_lidar(file)


def get_lidar_dtype(extension: str) -> np.dtype:
    """
    Constructs a lidar parsing np.dtype according to file extension

    :param extension: lidar file extension, valid exentions are 'ldo'/'ldg'/'ldx',
    passing an invalid string will raise a ValueError

    :return: np.dtype that can be used to parse the file with all fields
    """
    if extension not in ["ldo", "ldg", "ldx"]:
        raise ValueError(f"Invalid flie type passed: {extension}")

    lidar_dtype = [('x', np.float32), ('y', np.float32), ('z', np.float32),
                   ('delta_time', np.float16),
                   ('lidar_identifier', np.uint8),
                   ('intensity', np.uint8)]

    if extension != 'ldo':
        lidar_dtype.extend([('classInstance', np.uint32),
                            ('lidar_mat_id', np.uint16),
                            ('normal_cos', np.float16),
                            ('StructurePointindex', np.uint32),
                            ('reference_distance', np.float16),
                            ('fillfactor', np.uint8),
                            ('reference_reflectivity', np.uint8)])
        if extension != 'ldg':
            lidar_dtype.extend([('normal angle theta', np.float16),
                                ('normal angle phi', np.float16),
                                ('place holder1', np.float32),
                                ('place holder2', np.float32),
                                ('place holder3', np.float32),
                                ('place holder4', np.float32),
                                ('place holder5', np.float32),
                                ('place holder6', np.float32),
                                ('place holder7', np.float32)])

    return np.dtype(lidar_dtype)


def decode_lidar(file: str, extension: str = '') -> pd.DataFrame:
    """
    Decode Lidar binary data and returns pd dataframe

    :param file: absolute path to binary lidar data file
    :param extension: optional - indicates type of lidar file (valid values: 'ldo','ldg','ldx')

    :return: dataframe holding the parsed lidar data
    """
    if not extension:
        extension = pathlib.Path(file).suffix[1:]
    lidar_dtype = get_lidar_dtype(extension)
    data = np.fromfile(file, lidar_dtype)
    if extension != 'ldo':
        # separate combo values
        object_class = data['classInstance'] >> 24
        object_instance = data['classInstance'] & 0xffffff
        object_structure = data['StructurePointindex'] >> 24
        object_pointindex = data['StructurePointindex'] & 0xffffff
        fill_nominator = (data['fillfactor'] >> 4) + 1
        fill_denominator = (data['fillfactor'] & 0xf) + 1
        # remove unneeded fields and add intensity and ring to data structure
        data = recfunctions.drop_fields(data, DROPPED_FIELDS)
        data = recfunctions.append_fields(data, ['Class', 'ID', 'part_id', 'point_idx', 'nominator', 'denominator'],
                                          [object_class, object_instance, object_structure, object_pointindex,
                                           fill_nominator, fill_denominator])
    data = pd.DataFrame.from_records(data).reindex(LIDAR_COLUMN_NAMES, axis=1)
    data[ZERO_FILL] = data[ZERO_FILL].fillna(0)
    data[MINUS_FILL] = data[MINUS_FILL].fillna(-1)
    return data

#----------------------------------------------------------------------------------------------------------# Romano's code beneath

def run(TEST_PATH):
    
    empty = pd.DataFrame()
    # print(TEST_PATH[TEST_PATH.find('/'):])
    record = TEST_PATH[TEST_PATH.find('/'):]
    output_dir = f'RomanosConvertedLidar{record}'
    makeAnOutput(output_dir)
    print(LIGHT_BLUE + f"\nConvert ldo to csv from {TEST_PATH} to {output_dir}" + END)
    # sys.exit()
    for i, file in enumerate(sorted(os.listdir(TEST_PATH))):
        
        cur_path = os.path.join(TEST_PATH, file)
        lidar_data = decode_lidar(cur_path) 
        
        output_path = os.path.join(output_dir, file)
        output_path = output_path[:output_path.rfind('.')+1]+'csv'

        lidar_data.to_csv(output_path) #viewing in cloud compare
        print(GREEN + f"Epoch number {i+1} : {output_path} been created successfully!" + END)
        # os.remove(cur_path)
    print('\n\n\n')





def main():
    
    # TEST_PATH = "/home/simteamq/Desktop/lidar-analysis/velodyne32e_21700001"
    # TEST_PATH = "8 velodyne 28.5.24/664ef7aa8c2505002bd3728d/Velodyne_32E_Hatal110001"
    
    target_directory = "8 velodyne 28.5.24"
    tests_pathes = [f'{target_directory}/{name}/Velodyne_32E_Hatal110001' for name in os.listdir(target_directory) if os.path.isdir(os.path.join(target_directory, name))]
    
    # makeAnOutput(directory_name = "RomanosConvertedLidar")

    
    for test_path in tests_pathes:
        # print(test_path)
        run(TEST_PATH=test_path)

    

    

    # lidar_data = decode_lidar(TEST_PATH)
    # lidar_data.to_csv('output.csv') #viewing in cloud compare
    
    """
    # lidar_filtered = pd.DataFrame()
    # maxium = -1
    # max_point = []
    # x, y, z = [], [], []
    # for file in os.listdir(TEST_PATH):
    #     cur_path = os.path.join(TEST_PATH, file)
    #     lidar_data = decode_lidar(cur_path)
    #     for rowIndex, row in lidar_data.iterrows():
    #         if float(size(row['x'], row['y'], row['z'])) < 7.2 and float(size(row['x'], row['y'], row['z'])) > 6.5: 
    #             dist = math.sqrt(size(row['x'], row['y'], row['z'])**2 - (3.53)**2)
    #             if(dist > maxium):
    #                 maxium = dist
    #                 max_point = row['x'], row['y'], row['z']
    #             x.append(row['x'])
    #             y.append(row['y'])
    #             z.append(row['z'])
    # lidar_filtered['X'] = x
    # lidar_filtered['Y'] = y
    # lidar_filtered['Z'] = z

    # slope = 0.8/3.53
    # hyp = size(row['x'], row['y'], row['z'])**2
    # print(hyp*slope)

    # lidar_filtered.to_csv("d9.csv")

# TEST_PATH = r"/home/shahaf/Downloads/Velodyne32eShahaf0001"

# if __name__ == "__main__" and TEST_PATH:
#     lidar_filtered = pd.DataFrame()
#     x, y, z = [], [], []
#     count = 0
#     for file in os.listdir(TEST_PATH):
#         cur_path = os.path.join(TEST_PATH, file)
#         lidar_data = decode_lidar(cur_path)
#         for rowIndex, row in lidar_data.iterrows():
#             if float(size(row['x'], row['y'], row['z'])) < 3.3 and float(size(row['x'], row['y'], row['z'])) > 2.2 and row['x'] > 0 and row['z'] > -0.98: 
#                 count +=1
#                 x.append(row['x'])
#                 y.append(row['y'])
#                 z.append(row['z'])
#     print (count)  
#     lidar_filtered['X'] = x
#     lidar_filtered['Y'] = y
#     lidar_filtered['Z'] = z
#     lidar_filtered.to_csv("filtered.csv")
    """
        

if __name__ == "__main__":

    main()
    
    
    
