import skimage
import os
import sys
import numpy as np
import matplotlib.image
import matplotlib.pyplot as plt
from skimage.filters import threshold_mean
from PIL import Image

# Input files
style_file = sys.argv[1]
orig_file = sys.argv[2]
seg_file = sys.argv[3]

# Get style transfered image
st_im = Image.open(style_file)
st_arr = np.asarray(st_im)
st_arr = st_arr[:, :, 0:3]

# Get original image
orig_im = Image.open(orig_file)
orig_arr = np.asarray(orig_im)

# Get segmentation image
seg_im = Image.open(seg_file)
seg_arr = np.asarray(seg_im)

color_file = sys.argv[8]
if(not os.path.isfile(color_file)):
    # Input region
    x = sys.argv[4]
    y = sys.argv[5]
    x = float(x)
    y = float(y)
    x *= len(orig_arr[0])
    y *= len(orig_arr)
    x = int(x)
    y = int(y)
    color = seg_arr[y, x]
    np.savetxt(color_file, color)
else:
    color = np.loadtxt(color_file)

# Exclude
exclude = sys.argv[6]
exclude = bool(int(exclude))

# Set up output image
m, n, _ = orig_arr.shape
out_arr = np.zeros((m, n, 3))

# Write correct pixel to output based on binary
for i in range(m):
    for j in range(n):
        if(exclude):
            if(np.all(np.equal(np.around(color, decimals=3), np.around(seg_arr[i, j], decimals=3)))):
                out_arr[i, j] = orig_arr[i, j]
            else:
                out_arr[i, j] = st_arr[i, j]
        else:
            if(np.all(np.equal(np.around(color, decimals=3), np.around(seg_arr[i, j], decimals=3)))):
                out_arr[i, j] = st_arr[i, j]
            else:
                out_arr[i, j] = orig_arr[i, j]

# Save output image
outfilename = sys.argv[7]
matplotlib.image.imsave(outfilename, out_arr.astype(int))
