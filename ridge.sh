#!/bin/bash
declare -a arr=("-a=normalize=False,fit_intercept=False"
                "-a=normalize=True,fit_intercept=False"
                "-a=normalize=False,fit_intercept=True"
                "-a=normalize=True,fit_intercept=True"
                "-a=normalize=False,fit_intercept=False -u=true"
                "-a=normalize=True,fit_intercept=False -u=true"
                "-a=normalize=False,fit_intercept=True -u=true"
                "-a=normalize=True,fit_intercept=True -u=true"
                "-a=normalize=False,fit_intercept=False -u=true -f=method,url"
                "-a=normalize=True,fit_intercept=False -u=true -f=method,url"
                "-a=normalize=False,fit_intercept=True -u=true -f=method,url"
                "-a=normalize=True,fit_intercept=True -u=true -f=method,url"
                )

mkdir -p "results"
for i in "${arr[@]}"
do
   echo "$i"
   touch "results/ridge_$i"
   python src/limython.py -n=3 -l=100 -m=ridge -r=false -p=best-counter $i > "results/ridge_$i" &
done
