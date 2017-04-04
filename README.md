# Limython [![Build Status](https://travis-ci.org/jansyk13/limython.svg?branch=master)](https://travis-ci.org/jansyk13/limython)

Python wrapper for machine learning for diploma thesis.
## Guide
Can be run as python script with several mandatory parameters.
`python src/limython.py -p=best-counter -l=100 -n=3 -k=2 -r=false`

### Help
```
usage: limython.py [-h] -p PROCESSOR -n NODE_COUNT -l LIMIT [-k K_FOLDS] -m
                   MODEL [-a ARGUMENTS] [-u URL] [-ul URL_LIMIT] [-f FEATURES]
                   -r RUN

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSOR, --processor PROCESSOR
                        Request processor(simple-round-robin,best-counter)
  -n NODE_COUNT, --node-count NODE_COUNT
                        Node count for processor(1,2,3,...)
  -l LIMIT, --limit LIMIT
                        Data limit(to avoid running out of memory)
  -k K_FOLDS, --k-folds K_FOLDS
                        Number of folds for cross validation(higher better,
                        but computation more expensive)
  -m MODEL, --model MODEL
                        ML model(ols, lasso, ridge, sgd, tree)
  -a ARGUMENTS, --arguments ARGUMENTS
                        ML model arguments - kwargs separated with comma
  -u URL, --url URL     Flag whether url should be parsed into tree like
                        indicators
  -ul URL_LIMIT, --url-limit URL_LIMIT
                        Limit depth of tree hierarchy of dummy variable parsed
                        from urls
  -f FEATURES, --features FEATURES
                        List of features - comma separated
  -r RUN, --run RUN     'true' or 'false' whether to run full with processor
```

## Setup
* Using Python 3.5 (`sudo yum install python35 python35-virtualenv python35-pip`)
* To create virtual environment `virtualenv-3.5 ml`
* To source environment `source ~/envs3/ml/bin/activate`
* To install dependencies `pip3 install -r requirements.txt`

### To install
* C and C++ compilers `sudo yum install gcc gcc-c++`
* Cython `pip install cython`
* MySQL `sudo yum isntall mysql mysql-server`
* MySQL devel `sudo yum install mysql mysql-devel mysql-lib`
* BLAS prerequistes `sudo yum install automake autoconf libtool* gcc-gfortran`
* BLAS `sudo yum install lapack-devel blas-devel atlas-sse3-devel`

## Data
* using test data from http://ita.ee.lbl.gov/html/contrib/EPA-HTTP.html

## BLAS
* See configuration with NumPy `python -c "import numpy; numpy.show_config()"`
* See configuration with SciPy `python -c "import scipy; scipy.show_config()"`
* Make sure BLAS is setup correctly `export MKL_NUM_THREADS=32` `export OPENBLAS_NUM_THREADS=32` `export NUMEXPR_NUM_THREADS=32`
