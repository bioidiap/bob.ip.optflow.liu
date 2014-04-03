.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Tue  1 Apr 12:32:06 2014 CEST

.. image:: https://travis-ci.org/bioidiap/xbob.ip.optflow.liu.svg?branch=master
   :target: https://travis-ci.org/bioidiap/xbob.ip.optflow.liu
.. image:: https://coveralls.io/repos/bioidiap/xbob.ip.optflow.liu/badge.png
   :target: https://coveralls.io/r/bioidiap/xbob.ip.optflow.liu
.. image:: http://img.shields.io/github/tag/bioidiap/xbob.ip.optflow.liu.png
   :target: https://github.com/bioidiap/xbob.ip.optflow.liu
.. image:: http://img.shields.io/pypi/v/xbob.ip.optflow.liu.png
   :target: https://pypi.python.org/pypi/xbob.ip.optflow.liu
.. image:: http://img.shields.io/pypi/dm/xbob.ip.optflow.liu.png
   :target: https://pypi.python.org/pypi/xbob.ip.optflow.liu

=================================================
 Python Bindings to Liu's Optical Flow Framework
=================================================

This package is a simple Python wrapper to the open-source Optical Flow
estimator developed by C. Liu during his Ph.D. The code was originally
conceived to operate over Matlab. This is a Python/`Bob`_ port. If you use this
code, the author asks you to cite his thesis::

    @thesis{Liu_PHD_2009,
      title = {{Beyond Pixels: Exploring New Representations and Applications for Motion Analysis}},
      author = {Liu, C.},
      institution = {{Massachusetts Institute of Technology}},
      year = {2009},
      type = {{Ph.D. Thesis}},
    }

If you decide to use this port on your publication, we kindly ask you to cite
`Bob`_ as well, as the base software framework, on which this port has been
developed::

    @inproceedings{Anjos_ACMMM_2012,
      author = {A. Anjos and L. El Shafey and R. Wallace and M. G\"unther and C. McCool and S. Marcel},
      title = {Bob: a free signal processing and machine learning toolbox for researchers},
      year = {2012},
      month = oct,
      booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
      publisher = {ACM Press},
      url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},
    }

Here is a link `Liu's homepage`_ with details on the code, also displaying the
original Matlab port.

Installation
------------

Install it through normal means, via PyPI or use ``zc.buildout`` to bootstrap
the package and run test units.

Testing
-------

You can run a set of tests using the nose test runner::

  $ nosetests -sv xbob.ip.optflow.liu

.. warning::

   If Bob <= 1.2.1 is installed on your python path, nose will automatically
   load the old version of the insulate plugin available in Bob, which will
   trigger the loading of incompatible shared libraries (from Bob itself), in
   to your working binary. This will cause a stack corruption. Either remove
   the centrally installed version of Bob, or build your own version of Python
   in which Bob <= 1.2.1 is not installed.

You can run our documentation tests using sphinx itself::

  $ sphinx-build -b doctest doc sphinx

You can test overall test coverage with::

  $ nosetests --with-coverage --cover-package=xbob.ip.optflow.liu

The ``coverage`` egg must be installed for this to work properly.

Development
-----------

To develop this package, install using ``zc.buildout``, using the buildout
configuration found on the root of the package::

  $ python bootstrap.py
  ...
  $ ./bin/buildout

Tweak the options in ``buildout.cfg`` to disable/enable verbosity and debug
builds.

.. Place your references here:

.. _Bob: http://www.idiap.ch/software/bob/
.. _Liu's Homepage: http://people.csail.mit.edu/celiu/OpticalFlow/
