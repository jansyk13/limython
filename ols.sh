#!/bin/bash
# dont run this unless you want to experience freeeeeeeeeeeeeeze
declare -a arr=("-a=normalize=False,fit_intercept=False"
                "-a=normalize=True,fit_intercept=False"
                "-a=normalize=False,fit_intercept=True"
                "-a=normalize=True,fit_intercept=True"
                "-a=normalize=False,fit_intercept=False -u=true -ul=8"
                "-a=normalize=True,fit_intercept=False -u=true -ul=8"
                "-a=normalize=False,fit_intercept=True -u=true -ul=8"
                "-a=normalize=True,fit_intercept=True -u=true -ul=8"
                "-a=normalize=False,fit_intercept=False -u=true -ul=8 -f=method,url,payload_size"
                "-a=normalize=True,fit_intercept=False -u=true -ul=8 -f=method,url,payload_size"
                "-a=normalize=False,fit_intercept=True -u=true -ul=8 -f=method,url,payload_size"
                "-a=normalize=True,fit_intercept=True -u=true -ul=8 -f=method,url,payload_size"
                )

mkdir -p "results"
for i in "${arr[@]}"
do
   echo "$i"
   touch "results/ols_$i"
   python src/limython.py -n=3 -l=10000 -m=ols -r=false -p=best-counter -k=10 $i > "results/ols_$i" &
done
