#!/bin/bash
# dont run this unless you want to experience freeeeeeeeeeeeeeze
declare -a arr=("-a=loss=huber,fit_intercept=1"
                "-a=loss=epsilon_insensitive,fit_intercept=1"
                "-a=loss=squared_epsilon_insensitive,fit_intercept=1"
                "-a=loss=squared_loss,fit_intercept=0"
                "-a=loss=huber,fit_intercept=0"
                "-a=loss=epsilon_insensitive,fit_intercept=0"
                "-a=loss=squared_epsilon_insensitive,fit_intercept=0"
                "-a=loss=squared_loss,fit_intercept=1"
                "-a=loss=squared_loss,fit_intercept=1 -u=true -ul=8"
                "-a=loss=huber,fit_intercept=1 -u=true -ul=8"
                "-a=loss=epsilon_insensitive,fit_intercept=1 -u=true -ul=8"
                "-a=loss=squared_epsilon_insensitive,fit_intercept=1 -u=true -ul=8"
                "-a=loss=squared_loss,fit_intercept=0 -u=true -ul=8"
                "-a=loss=huber,fit_intercept=0 -u=true -ul=8"
                "-a=loss=epsilon_insensitive,fit_intercept=0 -u=true -ul=8"
                "-a=loss=squared_epsilon_insensitive,fit_intercept=0 -u=true -ul=8"
                "-a=loss=squared_epsilon_insensitive,fit_intercept=0 -u=true -ul=8 -f=method,url,payload_size"
                "-a=loss=squared_loss,fit_intercept=1 -u=true -ul=8 -f=method,url,payload_size"
                "-a=loss=huber,fit_intercept=1 -u=true -ul=8 -f=method,url,payload_size"
                "-a=loss=epsilon_insensitive,fit_intercept=1 -u=true -ul=8  -f=method,url,payload_size"
                "-a=loss=squared_loss,fit_intercept=0 -u=true -ul=8 -f=method,url,payload_size"
                "-a=loss=huber,fit_intercept=0 -u=true -ul=8 -f=method,url,payload_size"
                "-a=loss=epsilon_insensitive,fit_intercept=0 -u=true -ul=8 -f=method,url,payload_size"
                "-a=loss=epsilon_insensitive,fit_intercept=1 -u=true -ul=8 -f=method,url,payload_size"
                "-a=loss=squared_epsilon_insensitive,fit_intercept=1 -u=true -ul=8 -f=method,url,payload_size"
)

mkdir -p "results"
for i in "${arr[@]}"
do
   echo "$i"
   touch "results/sgd_$i"
   python src/limython.py -n=3 -l=10000 -m=sgd -r=false -p=best-counter -k=10 $i > "results/sgd_$i" &
done
