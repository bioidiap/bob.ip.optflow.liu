#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Thu 20 Sep 2012 14:43:19 CEST

"""Bindings for Liu's optical flow
"""

from setuptools import setup, find_packages, dist
dist.Distribution(dict(setup_requires=['bob.extension', 'bob.blitz']))
from bob.blitz.extension import Extension, build_ext

from bob.extension.utils import load_requirements
build_requires = load_requirements()

# Define package version
version = open("version.txt").read().rstrip()

setup(

    name="bob.ip.optflow.liu",
    version=version,
    description="Ce Liu's Optical Flow Framework for Bob",
    license="BSD",
    author='Andre Anjos',
    author_email='andre.anjos@idiap.ch',
    long_description=open('README.rst').read(),
    url='https://gitlab.idiap.ch/bob/bob.ip.optflow.liu',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    setup_requires = build_requires,
    install_requires = build_requires,

    entry_points = {
      'console_scripts': [
        'bob_of_liu.py = bob.ip.optflow.liu.script.flow:main',
      ],
    },

    ext_modules = [
      Extension("bob.ip.optflow.liu.version",
        [
          "bob/ip/optflow/liu/version.cpp",
        ],
        version = version,
      ),

      Extension("bob.ip.optflow.liu.sor",
        [
          "bob/ip/optflow/liu/sor_based/OpticalFlow.cpp",
          "bob/ip/optflow/liu/sor_based/GaussianPyramid.cpp",
          "bob/ip/optflow/liu/sor_based/Stochastic.cpp",
          "bob/ip/optflow/liu/sor_based/main.cpp",
        ],
        version = version,
      ),

      Extension("bob.ip.optflow.liu.cg",
        [
          "bob/ip/optflow/liu/cg_based/OpticalFlow.cpp",
          "bob/ip/optflow/liu/cg_based/GaussianPyramid.cpp",
          "bob/ip/optflow/liu/cg_based/main.cpp",
        ],
        version = version,
      ),
    ],

    cmdclass = {
      'build_ext': build_ext
    },

    classifiers = [
      'Framework :: Bob',
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Scientific/Engineering :: Image Recognition',
    ],

)
