# Limython [![Build Status](https://travis-ci.org/jansyk13/limython.svg?branch=master)](https://travis-ci.org/jansyk13/limython)
Repository containing source code for my diploma thesis at University of Economics, Prague. The topic is 'An Analysis of Potential Applications of Machine Learning in HTTP Load-balancing'. Repository contains Python and BASH wrappers for machine learning and simulating load balancing system. Full text of the thesis can be found in repository as well.

## Guide
Can be run as python script with several mandatory parameters(`limython.py`):<br />
`python src/limython.py -p=best-counter -l=100 -n=3 -k=2 -r=false`<br />
To get baselines of data use `baseline.py` script:<br />
`python src/baseline.py -n=3 -p=best-counter -k=10 -r=true -l=1000`<br />
To run final test use `final.py` script:<br />
`python src/final.py -p=best-counter -l=50000 -m=sgd -a=loss=huber,fit_intercept=1 -u=true -ul=8`

## Parsing log files to csv format
Run `result_to_csv.py` script with parameters `stdev|timer|rmse|rsquared|counter` and path `/results/` and then forward standard output to file.

## Database
Database should be running on localhost with port 3306. Current setup uses `root` as user and `password` as password, but it is easy to change by editing scripts.
Database schema should be named `mlrl` and table named `data`.

## Setup
* Install Fortran, C and C++ compilers (`yum install gcc-gfortran gcc gcc-c++`)
* Install MySQL server, command line client and other related libraries (`yum isntall mysql mysql-server mysql-devel mysql-lib`)
* Install BLAS prerequistes (`yum install automake autoconf libtool*`)
* Install BLAS (`yum install lapack-devel blas-devel atlas-sse3-devel`)
* Install Python 3.5 and virtualenv (`yum install python35 python35-virtualenv python35-pip`)
* Create and source new environment (`virtualenv-3.5 ml; source ml/bin/activate`)
* Install Cython via Pip (`pip install cython`)
* Install required dependencies in source code folder (`pip install -r requirements.txt`)

Note: Installation via Pip may cause compilation of several libraries into C and C++ and it can make it very slow(verbose mode recommended). Other issue is that Pip may not respect dependencies between libraries in requirements.txt(install separately).

## Data
* using test data from http://ita.ee.lbl.gov/html/contrib/EPA-HTTP.html

## BLAS
* See configuration with NumPy `python -c "import numpy; numpy.show_config()"`
* See configuration with SciPy `python -c "import scipy; scipy.show_config()"`
* Make sure BLAS is setup correctly `export MKL_NUM_THREADS=32` `export OPENBLAS_NUM_THREADS=32` `export NUMEXPR_NUM_THREADS=32`

### Help limython.py
```
usage: limython.py [-h] -p PROCESSOR -n NODE_COUNT -l LIMIT [-k K_FOLDS] -m
                   MODEL [-a ARGUMENTS] [-u URL] [-ul URL_LIMIT] [-f FEATURES]
                   -r RUN

Python wrapper to simulate load balancing system and to run tests.

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

### Help baseline.py
```
usage: baseline.py [-h] -p PROCESSOR -n NODE_COUNT -l LIMIT [-k K_FOLDS] -r
                   RUN

Python wrapper to simulate load balancing system and to create baselines.

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
  -r RUN, --run RUN     'true' or 'false' whether to run full with processor
```

### Help final.py
```
usage: final.py [-h] -p PROCESSOR -l LIMIT -m MODEL [-a ARGUMENTS] [-u URL]
                [-ul URL_LIMIT] [-f FEATURES]

Python wrapper to simulate load balancing system and to run tests for final
stage.

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSOR, --processor PROCESSOR
                        Request processor(simple-round-robin,best-counter)
  -l LIMIT, --limit LIMIT
                        Data limit(to avoid running out of memory)
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
```
