import lasio
import numpy as np
import matplotlib.pyplot as plt
import os

DATA_DIR = "..\\data\\las"
EXCEL_DIR = "data"

colors = {
    1: 'red',
    2: 'blue',
    3: 'green',
    4: 'yellow',
    5: 'orange',
    6: 'purple',
    7: 'cyan',
    8: 'magenta',
    9: 'lime',
    10: 'pink',
    11: 'teal',
    12: 'lavender',
    13: 'brown',
    14: 'maroon',
    15: 'olive'
}


def view_well(selected_well, target_layers, relative_index=True):
    if relative_index:
        las = lasio.read(os.path.join(DATA_DIR, f"{target_layers.iloc[selected_well]['Well identifier']}_continuous.las"))
        target_layer_idx = np.where((las['Z'] < target_layers.iloc[selected_well].upper) & (las['Z'] > target_layers.iloc[selected_well].lower))
        las_dis = lasio.read(os.path.join(DATA_DIR, f"{target_layers.iloc[selected_well]['Well identifier']}_discrete.las"))
        target_layer_idx_dis = np.where((las_dis['Z'] < target_layers.iloc[selected_well].upper) & (las_dis['Z'] > target_layers.iloc[selected_well].lower))
        background_ranges = las_dis['Z'][target_layer_idx_dis]
        background_ranges = np.append(background_ranges, las['Z'][target_layer_idx][-1])
        background_ranges = np.insert(background_ranges, 0, las['Z'][target_layer_idx][0])

        background_ranges = np.vstack((background_ranges[:-1], background_ranges[1:])).T

    else:
        las = lasio.read(os.path.join(DATA_DIR, f"{selected_well}_continuous.las"))
        target_layer_idx = np.where((las['Z'] < target_layers.loc[target_layers['Well identifier'] == selected_well].upper.values) & (las['Z'] > target_layers.loc[target_layers['Well identifier'] == selected_well].lower.values))

    background_colors = None
    try:
        background_colors = [colors[key] for key in las_dis['FACIES'][np.insert(target_layer_idx_dis, 0, target_layer_idx_dis[0][0]-1)].astype(int)]
    except KeyError:
        print('Probably not enough rows in discrete file, check number ', target_layers.iloc[selected_well]['Well identifier'])
    except IndexError:
        print('No points in chosen interval, check number ', target_layers.iloc[selected_well]['Well identifier'])
    
    plt.figure(figsize=(20, 4))
    plt.subplot(121)
    try:
        plt.plot(las["Z"][target_layer_idx], las["NEU"][target_layer_idx])
        no_neu_flag = False
    except KeyError:
        print("No NEU measurements in target layer")
        no_neu_flag = True
    if background_colors is not None:
        for color, (start, end) in zip(background_colors, background_ranges):
            plt.axvspan(start, end, color=color, alpha=0.3)

    plt.xlabel("Z")
    plt.ylabel("NEU")
    plt.subplot(122)
    try:
        plt.plot(las["Z"][target_layer_idx], las["GGKP"][target_layer_idx])
        no_ggkp_flag = False
    except KeyError:
        print("No GGKP measurements in target layer")
        no_ggkp_flag = True
    if background_colors is not None:    
        for color, (start, end) in zip(background_colors, background_ranges):
            plt.axvspan(start, end, color=color, alpha=0.3)


    plt.xlabel("Z")
    plt.ylabel("GGKP")
    plt.show()
    
    if no_neu_flag:
        return las["Z"][target_layer_idx], las["GGKP"][target_layer_idx], None
    elif no_ggkp_flag:
        return las["Z"][target_layer_idx], None, las["NEU"][target_layer_idx]
    else:
        return las["Z"][target_layer_idx], las["GGKP"][target_layer_idx], las["NEU"][target_layer_idx]