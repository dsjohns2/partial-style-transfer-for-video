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

# Find center of segmentation blob
color_count = 0
center = np.zeros(2)
for i in range(m):
    for j in range(n):
        if(np.all(np.equal(np.around(color, decimals=3), np.around(seg_arr[i, j], decimals=3)))):
            color_count += 1
            center += np.array([i, j])
center /= color_count
center = center.astype(int)

# Expand color
radius = int(sys.argv[4])
for i in range(m):
    for j in range(n):
        if((i - center[0])**2 + (j - center[1])**2 <= radius**2):
            out_arr[i, j] = color

# Save output image
outfilename = sys.argv[5]
matplotlib.image.imsave(outfilename, out_arr.astype(np.uint8))
