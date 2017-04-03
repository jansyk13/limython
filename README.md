# Limython [![Build Status](https://travis-ci.org/jansyk13/limython.svg?branch=master)](https://travis-ci.org/jansyk13/limython)
* using test data from http://ita.ee.lbl.gov/html/contrib/EPA-HTTP.html
* source ~/envs3/ml/bin/activate
* pip3 install -r requirements.txt
* Python 3.5.2
* Python from distribution repo of AMI Linux(AWS) `sudo yum install python35 python35-virtualenv python35-pip`
* MySQL devel `sudo yum install mysql mysql-devel mysql-lib`
* C and C++ compilers `sudo yum install gcc gcc-c++`
* Cython `pip install cython`
* BLAS prereq(build essentials + tools) `sudo yum install automake autoconf libtool* gcc-gfortran`
* BLAS `sudo yum install lapack-devel blas-devel atlas-sse3-devel`
* See BLAS `python -c "import numpy; numpy.show_config()"` `python -c "import scipy; scipy.show_config()"`
* Make sure BLAS is setup correctly `export MKL_NUM_THREADS=32` `export OPENBLAS_NUM_THREADS=32` `export NUMEXPR_NUM_THREADS=32`
