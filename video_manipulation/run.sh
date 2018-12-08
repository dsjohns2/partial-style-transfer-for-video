#!/bin/bash

# 1: description
# 2: input video path
# 3: x_value of target (0, 1)
# 4: y_value of target (0, 1)
# 5: number of bubble iterations
# 6: checkpoint style path
# 7: exclude/include target
# 8: 0-semantic segmentation, k>1-kmeans

## Make data directory
if [ ! -d data ]; then
mkdir data
fi

## Image segmentation
# Input videos to original frames
if [ ! -d data/${1}_original_images ]; then
mkdir data/${1}_original_images
sh vid_to_imgs.sh $1 $2
fi

# Actual segmentation
if [ ! -d data/${1}_segmentation_images ]; then
mkdir data/${1}_segmentation_images
# Semantic segmentation
if [ $8 -eq "0" ]; then
cd ../semantic-segmentation-pytorch
sh run.sh ../video_manipulation/data/${1}_original_images ../video_manipulation/data/${1}_segmentation_images
cd ../video_manipulation
# K-means
else
python k_means.py data/${1}_original_images data/${1}_segmentation_images $8 $3 $4
fi
fi

# Segmented frames to bubble segmented frames
if [ ! -d data/${1}_bubble_segmentation_images ]; then
mkdir data/${1}_bubble_segmentation_images
sh bubble_all.sh data/${1}_segmentation_images data/${1}_bubble_segmentation_images $3 $4 $5 ${1}_color.txt
fi

## Style Transfer
if [ ! -d data/${1}_styled_images ]; then
mkdir ./data/${1}_styled_images
cd ../fast-artistic-videos
sh stylizeVideo_deepflow.sh ../video_manipulation/${2} $6 ../video_manipulation/data/${1}_styled_images
cd ../video_manipulation
fi

## Combine
# Output combination of style and original frames
if [ ! -d data/${1}_partial_styled_images ]; then
mkdir data/${1}_partial_styled_images
sh combine_all.sh data/${1}_original_images data/${1}_bubble_segmentation_images data/${1}_styled_images data/${1}_partial_styled_images $3 $4 ${1}_color.txt $7
fi

# Output frames to output video
rm ./output/${1} -r
mkdir ./output/${1}
sh imgs_to_vid.sh data/${1}_partial_styled_images ./output/${1}/${1}_combined.mp4
sh imgs_to_vid.sh data/${1}_original_images ./output/${1}/${1}_original.mp4
sh imgs_to_vid.sh data/${1}_bubble_segmentation_images ./output/${1}/${1}_segmented.mp4
sh imgs_to_vid.sh data/${1}_styled_images ./output/${1}/${1}_styled.mp4

## Clean
rm ${1}_color.txt

