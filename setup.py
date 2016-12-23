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
      },
      install_requires=[
        'mysqlclient==1.3.9',
        'configparser==3.5.0',
      ]
     )
