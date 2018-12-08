#!/bin/bash

# 1: image file
# 2: x value
# 3: y value

python find_target.py $1 $2 $3
display target_file.png
rm target_file.png
