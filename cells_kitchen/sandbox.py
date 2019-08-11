## initializations
prefix = "F:\\cells_kitchen_files\\datasets\\images_"
labels_folder = "F:\\cells_kitchen_files\\labels\\"
suffixes = ['N.00.00', 'N.01.01', 'N.02.00', 'N.03.00.t', 'N.04.00.t', 'YST']

## look at some sweet, sweet vids
vid_num = 0

preview_vid(prefix+'K53', frames_to_show=np.inf, fps=100)

## check out instance_segmentation DataGenerator...

from cells_kitchen.instance_segmentation.data_generator import DataGenerator
from cells_kitchen.config import datasets
gen = DataGenerator(datasets)
import matplotlib.pyplot as plt
import numpy as np

##
dataset_ind = 2
plt.close('all')
fig, ax = plt.subplots(1, 3, sharex=True, sharey=True)
ax[0].imshow(gen.data.negative_eg_mask[dataset_ind])
ax[1].imshow(gen.data.positive_eg_mask[dataset_ind])
ax[2].imshow(np.max(gen.data.y[dataset_ind], axis=0))
