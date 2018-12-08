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

# Input region
x = sys.argv[2]
y = sys.argv[3]
x = float(x)
y = float(y)
x *= len(seg_arr[0])
y *= len(seg_arr)
x = int(x)
y = int(y)

# Set up output image
out_arr = np.copy(seg_arr)
m, n, _ = seg_arr.shape

# Expand color
for i in range(m):
    for j in range(n):
    	if(i == y or j == x):
    		out_arr[i, j] = np.zeros(len(out_arr[i, j]))

# Save output image
outfilename = "target_file.png"
matplotlib.image.imsave(outfilename, out_arr.astype(np.uint8))
