import numpy as np
import os
from matplotlib.image import imread, imsave
import matplotlib.pyplot as plt
import random
import sys

def k_means(A_file, outfile, x_pos, y_pos, iterations=30, num_centroids=4):
    # Initialize
    A = imread(A_file)
    A = np.reshape(A, (len(A)*len(A[0]), 3))
    centroids = np.zeros((num_centroids, 3))
    labels = np.zeros(len(A))
    for j in range(num_centroids):
        centroids[j] = A[random.randint(0, len(A)-1)]
    # Loop
    for k in range(iterations):
        print("Iteration: " + str(k))
        print(centroids)
        for i, x in enumerate(A): 
            best_label = -1    
            smallest_val = sys.maxsize
            for j, mu in enumerate(centroids):
                cur_val = np.linalg.norm(x-mu)**2
                if(cur_val < smallest_val):
                    smallest_val = cur_val
                    best_label = j
            labels[i] = best_label
        for j in range(len(centroids)):
            count = 0
            total = 0
            for i, x in enumerate(A):
                if(labels[i] == j):
                    count += 1
                    total += x.astype(float)
            if(count > 0):
                centroids[j] = total / count
    A = imread(A_file)
    x_pos = float(x_pos)
    y_pos = float(y_pos)
    x_pos *= len(A[0])
    y_pos *= len(A)
    x_pos = int(x_pos)
    y_pos = int(y_pos)
    target_color = A[y_pos, x_pos]
    new_centroids = np.zeros((num_centroids+1, 3))
    for i, centroid in enumerate(centroids):
        new_centroids[i] = centroid
    new_centroids[len(centroids)] = target_color
    centroids = new_centroids
    return centroids

def saveimages(centroids, A_file, num_centroids, outfile):
    print("Saving "+outfile)
    A_large = imread(A_file)
    A_large = np.copy(A_large)
    for i in range(len(A_large)):
        for j in range(len(A_large[0])):
            x = A_large[i, j]
            best_label = -1
            smallest_val = sys.maxsize
            for k, mu in enumerate(centroids):
                cur_val = np.linalg.norm(x-mu)**2
                if(cur_val < smallest_val):
                    smallest_val = cur_val
                    best_label = k
            A_large[i, j] = centroids[best_label]
    imsave(outfile, A_large)
    return A_large

# Main
orig_dir = sys.argv[1]
out_dir = sys.argv[2]
x = sys.argv[4]
y = sys.argv[5]
orig_file = orig_dir + "/image-0000001.png"
out_file = out_dir + "/image-0000001.png"
num_centroids = int(sys.argv[3])
centroids = k_means(orig_file, out_file, x, y, iterations=5, num_centroids=num_centroids)
for filename in os.listdir(orig_dir):
    saveimages(centroids, orig_dir+"/"+filename, num_centroids, out_dir+"/"+filename)
