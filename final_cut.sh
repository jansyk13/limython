#!/bin/bash
# dont run this unless you want to experience freeeeeeeeeeeeeeze
declare -a arr=("-a=criterion=mse,splitter=random,max_depth=20,max_features=log2 -u=true"
                "-a=criterion=mae,splitter=best,max_depth=20,max_features=log2"
                "-a=criterion=mse,splitter=best,max_depth=20,max_features=log2 -u=true"
                "-a=criterion=mae,splitter=random,max_depth=20,max_features=log2"
                "-a=criterion=mse,splitter=best,max_depth=20,max_features=log2"
                "-a=criterion=mse,splitter=random,max_depth=20,max_features=sqrt -u=true"
                "-a=criterion=mse,splitter=random,max_depth=20,max_features=log2"
                )

mkdir -p "results"
for i in "${arr[@]}"
do
   echo "$i"
   touch "results/tree_$i"
   python src/limython.py -n=3 -l=50000 -m=tree -r=true -p=best-counter -k=-1 $i > "results/tree_$i" &
done
