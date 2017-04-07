#!/bin/bash
# dont run this unless you want to experience freeeeeeeeeeeeeeze
declare -a arr=(
                "-l=1000 -a=criterion=mse,splitter=random,max_depth=20,max_features=log2 -u=true"
                "-l=10000 -a=criterion=mse,splitter=random,max_depth=20,max_features=log2 -u=true"
                "-l=50000 -a=criterion=mse,splitter=random,max_depth=20,max_features=log2 -u=true"
                "-l=1000 -a=criterion=mae,splitter=best,max_depth=20,max_features=log2"
                "-l=10000 -a=criterion=mae,splitter=best,max_depth=20,max_features=log2"
                "-l=50000 -a=criterion=mae,splitter=best,max_depth=20,max_features=log2"
                "-l=1000 -a=criterion=mse,splitter=best,max_depth=20,max_features=log2 -u=true"
                "-l=10000 -a=criterion=mse,splitter=best,max_depth=20,max_features=log2 -u=true"
                "-l=50000 -a=criterion=mse,splitter=best,max_depth=20,max_features=log2 -u=true"
                "-l=1000 -a=criterion=mae,splitter=random,max_depth=20,max_features=log2"
                "-l=10000 -a=criterion=mae,splitter=random,max_depth=20,max_features=log2"
                "-l=50000 -a=criterion=mae,splitter=random,max_depth=20,max_features=log2"
                "-l=1000 -a=criterion=mse,splitter=best,max_depth=20,max_features=log2"
                "-l=10000 -a=criterion=mse,splitter=best,max_depth=20,max_features=log2"
                "-l=50000 -a=criterion=mse,splitter=best,max_depth=20,max_features=log2"
                "-l=1000 -a=criterion=mse,splitter=random,max_depth=20,max_features=sqrt -u=true"
                "-l=10000 -a=criterion=mse,splitter=random,max_depth=20,max_features=sqrt -u=true"
                "-l=50000 -a=criterion=mse,splitter=random,max_depth=20,max_features=sqrt -u=true"
                "-l=1000 -a=criterion=mse,splitter=random,max_depth=20,max_features=log2"
                "-l=10000 -a=criterion=mse,splitter=random,max_depth=20,max_features=log2"
                "-l=50000 -a=criterion=mse,splitter=random,max_depth=20,max_features=log2"
                )

mkdir -p "results"
for i in "${arr[@]}"
do
   echo "$i"
   touch "results/tree_$i"
   python src/final.py -m=tree -p=best-counter $i > "results/tree_$i" &
   sleep 60 # contains sleep to avoid running out of memory and allow it to run on instance with less memory(only 60 GB)
done
