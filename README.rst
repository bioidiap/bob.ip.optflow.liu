.. vim: set fileencoding=utf-8 :
.. Mon 15 Aug 2016 18:41:03 CEST

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.ip.optflow.liu/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.ip.optflow.liu/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.ip.optflow.liu/badges/v2.0.9/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.optflow.liu/commits/v2.0.9
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.optflow.liu
.. image:: http://img.shields.io/pypi/v/bob.ip.optflow.liu.png
   :target: https://pypi.python.org/pypi/bob.ip.optflow.liu
.. image:: http://img.shields.io/pypi/dm/bob.ip.optflow.liu.png
   :target: https://pypi.python.org/pypi/bob.ip.optflow.liu


======================================
 Liu's Optical Flow Framework for Bob
======================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains a simple Python wrapper to the open-source Optical Flow
estimator developed by C. Liu during his Ph.D.  The code was originally
conceived to operate over Matlab. This is a Python/`Bob`_ port.  If you use
this code, the author asks you to cite his thesis::

  @phdthesis{Liu_PHD_2009,
    title = {{Beyond Pixels: Exploring New Representations and Applications for Motion Analysis}},
    author = {Liu, Ce},
    institution = {{Massachusetts Institute of Technology}},
    year = {2009},
    type = {{Ph.D. Thesis}},
  }


Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel
.. _liu's homepage: http://people.csail.mit.edu/celiu/OpticalFlow
