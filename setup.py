#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Thu 20 Sep 2012 14:43:19 CEST 

"""Bindings for flandmark
"""

import sys
import subprocess
from setuptools import setup, find_packages
from distutils.extension import Extension

def pkgconfig(package):

  def uniq(seq, idfun=None):
    # order preserving
    if idfun is None:
      def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
      marker = idfun(item)
      # in old Python versions:
      # if seen.has_key(marker)
      # but in new ones:
      if marker in seen: continue
      seen[marker] = 1
      result.append(item)
    return result

  flag_map = {
      '-I': 'include_dirs',
      '-L': 'library_dirs',
      '-l': 'libraries',
      }

  cmd = [
      'pkg-config',
      '--libs',
      '--cflags',
      package,
      ]

  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT)

  output = proc.communicate()[0]

  if proc.returncode != 0:
    raise RuntimeError, "PkgConfig did not find package %s. Output:\n%s" % \
        (package, output.strip())

  kw = {}

  for token in output.split():
    if flag_map.has_key(token[:2]):
      kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])

    elif token[0] == '-': # throw others to extra_link_args
      kw.setdefault('extra_compile_args', []).append(token)

    else: # these are maybe libraries
      if os.path.exists(token):
        dirname = os.path.dirname(token)
        if dirname not in kw.get('library_dirs', []):
          kw.setdefault('library_dirs', []).append(dirname)

        bname = os.path.splitext(os.path.basename(token))[0][3:]
        if bname not in kw.get('libraries', []):
          kw.setdefault('libraries', []).append(bname)

  for k, v in kw.iteritems(): # remove duplicated
    kw[k] = uniq(v)

  return kw

def setup_bob_extension(ext_name, sources):
  """Sets up a given C++ extension that depends on Bob"""

  bob = pkgconfig('bob-python')

  return Extension(
      ext_name,
      sources=sources,
      language="c++",
      include_dirs=bob.get('include_dirs',[]) + ['xbob/optflow/liu/ext'],
      library_dirs=bob.get('library_dirs',[]),
      runtime_library_dirs=bob.get('library_dirs',[]),
      libraries=bob.get('libraries',[]),
      )

setup(

    name="xbob.optflow.liu",
    version="1.0.0",
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

    install_requires=[
      'setuptools',
      'bob',
      ],

    entry_points = {
      'console_scripts': [
        'optflow_liu.py = xbob.optflow.liu.script.flow:main',
        ],
      },

    ext_modules=[
      setup_bob_extension("xbob.optflow.liu._liu",
        [
          "xbob/optflow/liu/ext/ext.cpp",
          "xbob/optflow/liu/ext/OpticalFlow.cpp",
          "xbob/optflow/liu/ext/GaussianPyramid.cpp",
          "xbob/optflow/liu/ext/Stochastic.cpp",
        ])
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
