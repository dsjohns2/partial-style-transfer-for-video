import skimage
import os
import sys
import numpy as np
import matplotlib.image
import matplotlib.pyplot as plt
from skimage.filters import threshold_mean
from PIL import Image

# Input files
seg_file = sys.argv[1]

# Get segmentation image
seg_im = Image.open(seg_file)
seg_arr = np.asarray(seg_im)

color_file = sys.argv[6]
if(not os.path.isfile(color_file)):
    # Input region
    x = sys.argv[2]
    y = sys.argv[3]
    x = float(x)
    y = float(y)
    x *= len(seg_arr[0])
    y *= len(seg_arr)
    x = int(x)
    y = int(y)
    color = seg_arr[y, x]
    np.savetxt(color_file, color)
else:
    color = np.loadtxt(color_file)

# Set up output image
out_arr = np.copy(seg_arr)
m, n, _ = seg_arr.shape

# Expand color
iterations = int(sys.argv[4])
for k in range(iterations):
    for i in range(1, m-1):
        for j in range(1, n-1):
            if(np.all(np.equal(np.around(color, decimals=3), np.around(seg_arr[i, j], decimals=3)))):
                out_arr[i, j] = color
                out_arr[i-1, j-1] = color
                out_arr[i-1, j+1] = color
                out_arr[i+1, j-1] = color
                out_arr[i+1, j+1] = color
                out_arr[i, j-1] = color
                out_arr[i, j+1] = color
                out_arr[i-1, j] = color
                out_arr[i+1, j] = color
    seg_arr = np.copy(out_arr) 

# Save output image
outfilename = sys.argv[5]
matplotlib.image.imsave(outfilename, out_arr.astype(np.uint8))
