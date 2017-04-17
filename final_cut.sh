#!/bin/bash
# dont run this unless you want to experience freeeeeeeeeeeeeeze
declare -a arr=(
                "-l=1000 -m=lasso -a=normalize=False,fit_intercept=True,positive=False,selection=random -u=true -ul=8 -f=method,url,payload_size"
                "-l=10000 -m=lasso -a=normalize=False,fit_intercept=True,positive=False,selection=random -u=true -ul=8 -f=method,url,payload_size"
                "-l=50000 -m=lasso -a=normalize=False,fit_intercept=True,positive=False,selection=random -u=true -ul=8 -f=method,url,payload_size"
                "-l=1000 -m=tree -a=criterion=mse,splitter=best,max_depth=10,max_features=auto -u=true -ul=8"
                "-l=10000 -m=tree -a=criterion=mse,splitter=best,max_depth=10,max_features=auto -u=true -ul=8"
                "-l=50000 -m=tree -a=criterion=mse,splitter=best,max_depth=10,max_features=auto -u=true -ul=8"
                "-l=1000 -m=sgd -a=loss=huber,fit_intercept=1 -u=true -ul=8"
                "-l=10000 -m=sgd -a=loss=huber,fit_intercept=1 -u=true -ul=8"
                "-l=50000 -m=sgd -a=loss=huber,fit_intercept=1 -u=true -ul=8"
                )

mkdir -p "results"
for i in "${arr[@]}"
do
   echo "$i"
   touch "results/final_$i"
   python src/final.py -p=best-counter $i > "results/final_$i" &
done
