# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 15:46:55 2013

@author: tillsten
"""

from distutils.core import setup

setup(name='qt-dataflow',
      version='0.2',
      description='A base for custom visual programming enviroments',
      author='Till Stensitzki',
      author_email='tillsten@zedat.fu-berlin.de',
      url='https://github.com/Tillsten/qt-dataflow',
      packages=['qtdataflow', 'qtdataflow.examples', 'qtdataflow.tests'],
      package_data={'qtdataflow.examples': ['icons/*.png']},        
     )