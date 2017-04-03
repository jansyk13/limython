#!/usr/bin/env python

from distutils.core import setup

setup(name='limython',
      version='0.1.0',
      description='Machine learning backed load balancing',
      author='Jan Sykora',
      author_email='jansyk13@gmail.com',
      packages=['src'],
      package_dir={
        'models': 'src/models',
        'processors': 'src/processors',
        'transformation': 'src/transformation',
        'data': 'src/data',
        'learning': 'src/learning',
      },
      install_requires=[
        'mysqlclient==1.3.9',
        'configparser==3.5.0',
        'numpy==1.12.1',
        'scipy==0.19.0'
        'pandas==0.19.2',
        'statsmodels==0.6.1',
        'scikit-learn==0.18.1'
        'pytest==3.0.7',
      ]
     )
