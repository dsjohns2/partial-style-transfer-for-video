#!/bin/bash

# 1: segmentation directory
# 2: bubble segmentation directory
# 3: x value
# 4: y value
# 5: number of iterations
# 6: colorfile

rm $6
for filename in $( ls $1 )
do
python bubble.py $1/$filename $3 $4 $5 $2/$filename $6
done
