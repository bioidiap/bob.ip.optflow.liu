.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Tue  1 Apr 12:32:06 2014 CEST

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.ip.optflow.liu/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.ip.optflow.liu/master/index.html
.. image:: https://travis-ci.org/bioidiap/bob.ip.optflow.liu.svg?branch=v2.0.5
   :target: https://travis-ci.org/bioidiap/bob.ip.optflow.liu
.. image:: https://coveralls.io/repos/bioidiap/bob.ip.optflow.liu/badge.png
   :target: https://coveralls.io/r/bioidiap/bob.ip.optflow.liu
.. image:: https://img.shields.io/badge/github-master-0000c0.png
   :target: https://github.com/bioidiap/bob.ip.optflow.liu/tree/master
.. image:: http://img.shields.io/pypi/v/bob.ip.optflow.liu.png
   :target: https://pypi.python.org/pypi/bob.ip.optflow.liu
.. image:: http://img.shields.io/pypi/dm/bob.ip.optflow.liu.png
   :target: https://pypi.python.org/pypi/bob.ip.optflow.liu

=========================================================
 Python Bindings to Liu's Optical Flow Framework for Bob
=========================================================

This package is a simple Python wrapper to the open-source Optical Flow estimator developed by C. Liu during his Ph.D.
The code was originally conceived to operate over Matlab.
This is a Python/`Bob`_ port.
If you use this code, the author asks you to cite his thesis::

  @phdthesis{Liu_PHD_2009,
    title = {{Beyond Pixels: Exploring New Representations and Applications for Motion Analysis}},
    author = {Liu, Ce},
    institution = {{Massachusetts Institute of Technology}},
    year = {2009},
    type = {{Ph.D. Thesis}},
  }


If you decide to use this port on your publication, we kindly ask you to cite Bob_ as well, as the base software framework, on which this port has been developed::

  @inproceedings{Anjos_ACMMM_2012,
    author = {Anjos, Andr\'e AND El Shafey, Laurent AND Wallace, Roy AND G\"unther, Manuel AND McCool, Christopher AND Marcel, S\'ebastien},
    title = {Bob: a free signal processing and machine learning toolbox for researchers},
    year = {2012},
    month = oct,
    booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
    publisher = {ACM Press},
    url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},
  }

Please read `Liu's homepage`_ for details on the code, also displaying the original Matlab port.


Installation
------------
To install this package -- alone or together with other `Packages of Bob <https://github.com/idiap/bob/wiki/Packages>`_ -- please read the `Installation Instructions <https://github.com/idiap/bob/wiki/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.

Documentation
-------------
For further documentation on this package, please read the `Stable Version <http://pythonhosted.org/bob.ip.optflow.liu/index.html>`_ or the `Latest Version <https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.ip.optflow.liu/master/index.html>`_ of the documentation.
For a list of tutorials on this or the other packages ob Bob_, or information on submitting issues, asking questions and starting discussions, please visit its website.

.. _bob: https://www.idiap.ch/software/bob
.. _liu's homepage: http://people.csail.mit.edu/celiu/OpticalFlow
