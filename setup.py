#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Thu 20 Sep 2012 14:43:19 CEST 

"""Bindings for Liu's optical flow
"""

from setuptools import setup, find_packages, dist
dist.Distribution(dict(setup_requires='xbob.extension'))
from xbob.extension import Extension, build_ext

setup(

    name="xbob.optflow.liu",
    version="1.1.2",
    description="Python bindings to the optical flow framework by C. Liu",
    license="GPLv3",
    author='Andre Anjos',
    author_email='andre.anjos@idiap.ch',
    long_description=open('README.rst').read(),
    url='http://pypi.python.org/pypi/xbob.optflow.liu',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    namespace_packages=[
      "xbob",
      "xbob.optflow",
      ],

    setup_requires = [
      'xbob.extension'
      ],

    install_requires=[
      'setuptools',
      'bob',
      ],

    entry_points = {
      'console_scripts': [
        'optflow_liu.py = xbob.optflow.liu.script.flow:main',
        ],
      },

    cmdclass = {
      'build_ext': build_ext,
      },

    ext_modules=[
      Extension("xbob.optflow.liu._sor_based", #new implementation
        [
          "xbob/optflow/liu/sor_based/ext.cpp",
          "xbob/optflow/liu/sor_based/OpticalFlow.cpp",
          "xbob/optflow/liu/sor_based/GaussianPyramid.cpp",
          "xbob/optflow/liu/sor_based/Stochastic.cpp",
        ],
        ),
      Extension("xbob.optflow.liu._cg_based", #old implementation
        [
          "xbob/optflow/liu/cg_based/ext.cpp",
          "xbob/optflow/liu/cg_based/OpticalFlow.cpp",
          "xbob/optflow/liu/cg_based/GaussianPyramid.cpp",
        ],
        )
      ],

    classifiers = [
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Scientific/Engineering :: Image Recognition',
      ],
    
    )
