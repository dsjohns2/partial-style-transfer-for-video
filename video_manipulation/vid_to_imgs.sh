#!/bin/bash

# 1: description (e.g. car)
# 2: input video

ffmpeg -i $2 -vf scale=450:350 -f image2 data/${1}_original_images/image-%07d.png
