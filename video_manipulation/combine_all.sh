#!/bin/bash

# 1: original directory
# 2: segmentation directory
# 3: style directory
# 4: partial style directory
# 5: x value
# 6: y value
# 7: color_file
# 8: exclude/include target

rm $7
for filename in $( ls $3 )
do
python combine.py $3/$filename $1/$filename $2/$filename $5 $6 $8 $4/$filename $7
done
