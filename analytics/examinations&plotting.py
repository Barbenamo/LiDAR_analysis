import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from main_gather_data import generate_delta_df

def create_range_value(data):
    x_range = np.linspace(min(data), max(data), 15)
    y_values = [0] * len(x_range)  # contains counters that count how many samples fit in the specific area
    y_dict = {}
    h = x_range[1] - x_range[0]
    index = 0
    for i in range(0, len(data)):
        index = int((data[i] - x_range[0]) / h)
        y_values[int(index)] += 1
        index = f"{index * h}-{index * h + h}"
        if not index in y_dict.keys():
            y_dict[index] = []
        y_dict[index].append(data[i])
    return x_range, y_values

def plot_single_distrubution_graph(data, df):
    x_range1, y_values1 = create_range_value(data=np.array(data))
    g = sns.barplot(data=df, x=x_range1, y=y_values1)
    plt.grid(True)
    xlabels = ['{:,.3f}'.format(x) + ' mm' for x in x_range1 * 1000]
    g.set_xticklabels(xlabels)
    plt.xlabel('Error value')
    plt.ylabel('# of occurrences')
    plt.title(f'Delta')
    plt.show()

def plot_three_distrubution_graph(data1, data2, data3, df):
    x_range1, y_values1 = create_range_value(data=np.array(data1))
    x_range2, y_values2 = create_range_value(data=np.array(data2))
    x_range3, y_values3 = create_range_value(data=np.array(data3))
    plt.subplot(1, 3, 1)
    g = sns.barplot(data=df, x=x_range1, y=y_values1)
    plt.grid(True)
    plt.title('x')
    xlabels = ['{:,.1f}'.format(x) + ' mm' for x in x_range1 * 1000]
    g.set_xticklabels(xlabels)

    plt.subplot(1, 3, 2)
    g = sns.barplot(data=df, x=x_range2, y=y_values2)
    plt.title('y')
    plt.grid()
    g.set_xticklabels(xlabels)

    plt.subplot(1, 3, 3)
    g = sns.barplot(data=df, x=x_range3, y=y_values3)
    plt.title('z')
    plt.grid(True)
    g.set_xticklabels(xlabels)

    plt.xlabel('Error value')
    plt.ylabel('# of occurrences')
    plt.show()

def read_data_from_df(df):
    del_x = df['x']
    del_y = df['y']
    del_z = df['z']
    noises = df['noise']
    return del_x, del_y, del_z, noises

def plot_delta_function(df):
    mean_x, mean_y, mean_z, noises = read_data_from_df(df)
    plt.subplot(1,3,1)
    plt.grid()
    plt.title('x')
    plt.plot(noises,mean_x)
    
    plt.subplot(1,3,2)
    plt.grid()
    plt.title('y')
    plt.plot(noises,mean_y)
    
    plt.subplot(1,3,3)
    plt.grid()
    plt.title('z')
    plt.plot(noises,mean_z)
    plt.show()

if __name__ == '__main__':        
    path = '/home/simteamq/Desktop/lidar-analysis/results'
    reference_file = '/home/simteamq/Desktop/lidar-analysis/nn_run_include_normal.csv'
    df_pcY_maxes = pd.read_csv(f'{path}/max_deltas_100_PCY3.csv')
    df_pcY_means = pd.read_csv(f'{path}/mean_deltas_100_PCY3.csv')
    df_pcY_deltas = pd.read_csv(f'{path}/deltas_100_PCY3.csv')

    df_pcZ_maxes = pd.read_csv(f'{path}/max_deltas_90_pcZ.csv')
    df_pcZ_deltas = pd.read_csv(f'{path}/mean_deltas_90_pcZ.csv')
    df_pcZ_means = pd.read_csv(f'{path}/deltas_90_pcZ.csv')

    del_x, del_y, del_z, noises = read_data_from_df(df_pcZ_deltas)

    plot_single_distrubution_graph(del_z,df_pcZ_deltas)
    plot_delta_function(df_pcZ_deltas)
    plot_delta_function(df_pcZ_maxes)
    plot_delta_function(df_pcZ_means)
    