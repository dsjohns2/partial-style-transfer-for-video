#!/bin/bash

# 1: combined images directory
# 2: output video file name

ffmpeg -pattern_type glob -i "$1/*.png" -c:v libx264 -pix_fmt yuv420p $2
