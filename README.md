# Limython [![Build Status](https://travis-ci.org/jansyk13/limython.svg?branch=master)](https://travis-ci.org/jansyk13/limython)
The repository containing the source code for my diploma thesis at University of Economics, Prague. The topic is 'An Analysis of Potential Applications of Machine Learning in HTTP Load-balancing'. the repository contains Python and BASH wrappers for machine learning and simulating load balancing system. the full text of the thesis can be found in the repository as well.

## Thesis
* Thesis was successfully defended in summer 2017.
* Supervisor: Ing. Rudfolf Pecinovsky, CSc.
* Oponent: Mgr. Zbynek Slajchrt, Ph.D.

### Title
An Analysis of Potential Applica-tions of Machine Learning in HTTP Load Balancing

### Abstract
Both machine learning and HTTP load balancing are well known and widely researched concepts and methods. My diploma thesis addresses possible applications of machine learning to HTTP load balancing. The main objective is to find a method to achieve better utilization of load balancing. This objective can reduce monetary costs and provide better stability of a load balanced system. In the first part, machine learning workflow and methods are described in order to analyze whether such methods could be applied to load balancing systems. After that, the current state of HTTP load balancing methods and strategies is outlined. Finally, a load balancing method using machine learning is designed and tested. The method is based on the least loaded approach using predicted values to balance HTTP traffic, the machine learning models were selected by using a grid search to find the most accurate models. These meth-ods were tested and performed well in comparison to other methods. The tests were conducted with over a hundred machine learning models, not all models were accurate or had short enough learning times. Lacking those factors deemed them unsuitable for later tests. The models were compared based on measured utilization and performance metrics for regression based machine learning models. The designed method could be applied to real world systems, however, it would require defining a domain specific metric. The applications should also employ a grid search in order to find the most accurate machine learning model.

### Keywords
HTTP protocol, load balancing, machine learning

## Guide
Can be run as python script with several mandatory parameters (`limython.py`):<br />
`python src/limython.py -p=best-counter -l=100 -n=3 -k=2 -r=false`<br />
To get baselines of data use `baseline.py` script:<br />
`python src/baseline.py -n=3 -p=best-counter -k=10 -r=true -l=1000`<br />
To run final test use `final.py` script:<br />
`python src/final.py -p=best-counter -l=50000 -m=sgd -a=loss=huber,fit_intercept=1 -u=true -ul=8`

## Parsing log files to csv format
Run `result_to_csv.py` script with parameters `stdev|timer|rmse|rsquared|counter` and path `/results/` and then forward standard output to file.

## Database
Database should be running on `localhost` with port `3306`. Current setup uses `root` as user and `password` as password, but it is easy to change by editing scripts.
Database schema should be named `mlrl` and table named `data`.

## Setup
* Install Fortran, C and C++ compilers (`yum install gcc-gfortran gcc gcc-c++`)
* Install MySQL server, command line client and other related libraries (`yum isntall mysql mysql-server mysql-devel mysql-lib`)
* Install BLAS prerequisites (`yum install automake autoconf libtool*`)
* Install BLAS (`yum install lapack-devel blas-devel atlas-sse3-devel`)
* Install Python 3.5 and virtualenv (`yum install python35 python35-virtualenv python35-pip`)
* Create and source new environment (`virtualenv-3.5 ml; source ml/bin/activate`)
* Install Cython via Pip (`pip install cython`)
* Install required dependencies in source code folder (`pip install -r requirements.txt`)

Note: Installation via Pip may cause compilation of several libraries into C and C++ and it can make it very slow(verbose mode recommended). Other issue is that Pip may not respect dependencies between libraries in requirements.txt(install separately).

## Data
* Using test data from http://ita.ee.lbl.gov/html/contrib/EPA-HTTP.html

## BLAS
* See configuration with NumPy `python -c "import numpy; numpy.show_config()"`
* See configuration with SciPy `python -c "import scipy; scipy.show_config()"`
* Make sure BLAS is set up correctly by setting to environment variables:
  * `export MKL_NUM_THREADS=32` 
  * `export OPENBLAS_NUM_THREADS=32` 
  * `export NUMEXPR_NUM_THREADS=32`

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
