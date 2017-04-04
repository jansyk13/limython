#!/bin/bash
# dont run this unless you want to experience freeeeeeeeeeeeeeze
declare -a arr=("-a=solver=svd,normalize=True,fit_intercept=False"
                 "-a=solver=cholesky,normalize=True,fit_intercept=False"
                 "-a=solver=lsqr,normalize=True,fit_intercept=False"
                 "-a=solver=sparse_cg,normalize=True,fit_intercept=False"
                 "-a=solver=sag,normalize=True,fit_intercept=False"
                 "-a=solver=svd,normalize=False,fit_intercept=False"
                 "-a=solver=cholesky,normalize=False,fit_intercept=False"
                 "-a=solver=lsqr,normalize=False,fit_intercept=False"
                 "-a=solver=sparse_cg,normalize=False,fit_intercept=False"
                 "-a=solver=sag,normalize=False,fit_intercept=False"
                 "-a=solver=svd,normalize=True,fit_intercept=True"
                 "-a=solver=cholesky,normalize=True,fit_intercept=True"
                 "-a=solver=lsqr,normalize=True,fit_intercept=True"
                 "-a=solver=sparse_cg,normalize=True,fit_intercept=True"
                 "-a=solver=sag,normalize=True,fit_intercept=True"
                 "-a=solver=svd,normalize=False,fit_intercept=True"
                 "-a=solver=cholesky,normalize=False,fit_intercept=True"
                 "-a=solver=lsqr,normalize=False,fit_intercept=True"
                 "-a=solver=sparse_cg,normalize=False,fit_intercept=True"
                 "-a=solver=sag,normalize=False,fit_intercept=True"
                 "-a=solver=svd,normalize=True,fit_intercept=False -u=true"
                 "-a=solver=cholesky,normalize=True,fit_intercept=False -u=true"
                 "-a=solver=lsqr,normalize=True,fit_intercept=False -u=true"
                 "-a=solver=sparse_cg,normalize=True,fit_intercept=False -u=true"
                 "-a=solver=sag,normalize=True,fit_intercept=False -u=true"
                 "-a=solver=svd,normalize=False,fit_intercept=False -u=true"
                 "-a=solver=cholesky,normalize=False,fit_intercept=False -u=true"
                 "-a=solver=lsqr,normalize=False,fit_intercept=False -u=true"
                 "-a=solver=sparse_cg,normalize=False,fit_intercept=False -u=true"
                 "-a=solver=sag,normalize=False,fit_intercept=False -u=true"
                 "-a=solver=svd,normalize=True,fit_intercept=True -u=true"
                 "-a=solver=cholesky,normalize=True,fit_intercept=True -u=true"
                 "-a=solver=lsqr,normalize=True,fit_intercept=True -u=true"
                 "-a=solver=sparse_cg,normalize=True,fit_intercept=True -u=true"
                 "-a=solver=sag,normalize=True,fit_intercept=True -u=true"
                 "-a=solver=svd,normalize=False,fit_intercept=True -u=true"
                 "-a=solver=cholesky,normalize=False,fit_intercept=True -u=true"
                 "-a=solver=lsqr,normalize=False,fit_intercept=True -u=true"
                 "-a=solver=sparse_cg,normalize=False,fit_intercept=True -u=true"
                 "-a=solver=sag,normalize=False,fit_intercept=True -u=true"
                 "-a=solver=svd,normalize=True,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=cholesky,normalize=True,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=lsqr,normalize=True,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=sparse_cg,normalize=True,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=sag,normalize=True,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=svd,normalize=False,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=cholesky,normalize=False,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=lsqr,normalize=False,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=sparse_cg,normalize=False,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=sag,normalize=False,fit_intercept=False -u=true -f=method,url,payload_size"
                 "-a=solver=svd,normalize=True,fit_intercept=True -u=true -f=method,url,payload_size"
                 "-a=solver=cholesky,normalize=True,fit_intercept=True -u=true -f=method,url,payload_size"
                 "-a=solver=lsqr,normalize=True,fit_intercept=True -u=true -f=method,url,payload_size"
                 "-a=solver=sparse_cg,normalize=True,fit_intercept=True -u=true -f=method,url,payload_size"
                 "-a=solver=sag,normalize=True,fit_intercept=True -u=true -f=method,url,payload_size"
                 "-a=solver=svd,normalize=False,fit_intercept=True -u=true -f=method,url,payload_size"
                 "-a=solver=cholesky,normalize=False,fit_intercept=True -u=true -f=method,url,payload_size"
                 "-a=solver=lsqr,normalize=False,fit_intercept=True -u=true -f=method,url,payload_size"
                 "-a=solver=sparse_cg,normalize=False,fit_intercept=True -u=true -f=method,url,payload_size"
                 "-a=solver=sag,normalize=False,fit_intercept=True -u=true -f=method,url,payload_size"
                )

mkdir -p "results"
for i in "${arr[@]}"
do
   echo "$i"
   touch "results/ridge_$i"
   python src/limython.py -n=3 -l=10000 -m=ridge -r=false -p=best-counter -k=10 $i > "results/ridge_$i" &
done
