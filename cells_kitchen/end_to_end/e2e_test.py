
from cells_kitchen.region_proposal.config import X_layers as rp_channels
from cells_kitchen.instance_segmentation.config import X_layers as is_channels
from cells_kitchen import utils
import numpy as np
from keras.models import load_model
import skimage.measure
import skimage.feature
import matplotlib.pyplot as plt


data_name = r'C:\Users\erica and rick\Desktop\cells_kitchen\training_data\K53.npz'
rp_model_name = r'C:\Users\erica and rick\Desktop\cells_kitchen\models\region_proposal\191006_21.09.28\unet.92-0.355555.hdf5'
is_model_name = r'C:\Users\erica and rick\Desktop\cells_kitchen\models\instance_segmentation\191007_20.01.09\segnet.99-0.367042.hdf5'

# load data and models
data = np.load(data_name, allow_pickle=True)['X'][()]
data_rp = np.stack([data[k] for k in rp_channels], axis=-1)
data_is = np.stack([data[k] for k in is_channels], axis=-1)
model_rp = load_model(rp_model_name)
model_is = load_model(rp_model_name)

# get region proposals
rp = model_rp.predict(np.expand_dims(data_rp, 0)).squeeze()

# get local maxima
maxima = skimage.feature.peak_local_max(rp, min_distance=2, threshold_abs=.2, indices=False)
labels = skimage.measure.label(maxima, 8)
regions = skimage.measure.regionprops(labels)
centroids = np.array([r.centroid for r in regions])

## show image
# plt.close('all')
# fig, ax = plt.subplots(1, 1)
ax.clear()
# ax.imshow(rp)
# ax.plot(centroids[:, 1], centroids[:, 0], 'r.')
subframe = get_subimg(rp, (-50, -200, 1000, 2000), padding='zeros')
ax.imshow(subframe)

## perform instance segmentation at each maximum









