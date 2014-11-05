.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Thu  3 Apr 13:47:28 2014 CEST
..
.. Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland

.. _bob.ip.optflow.liu:

=================================================
 Python Bindings to Liu's Optical Flow Framework
=================================================

.. todolist::

This package is a simple Python wrapper to the open-source Optical Flow estimator developed by C. Liu during his Ph.D.
The code was originally conceived to operate over Matlab.
This is a Python/`Bob`_ port.
If you use this code, the author asks you to cite his thesis:

.. code-block:: latex

  @phdthesis{Liu_PHD_2009,
    title = {{Beyond Pixels: Exploring New Representations and Applications for Motion Analysis}},
    author = {Liu, Ce},
    institution = {{Massachusetts Institute of Technology}},
    year = {2009},
    type = {{Ph.D. Thesis}},
  }

If you decide to use this port on your publication, we kindly ask you to cite Bob_ as well, as the base software framework, on which this port has been developed:

.. code-block:: latex

  @inproceedings{Anjos_ACMMM_2012,
    author = {Anjos, Andr\'e AND El Shafey, Laurent AND Wallace, Roy AND G\"unther, Manuel AND McCool, Christopher AND Marcel, S\'ebastien},
    title = {Bob: a free signal processing and machine learning toolbox for researchers},
    year = {2012},
    month = oct,
    booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
    publisher = {ACM Press},
    url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},
  }

Documentation
-------------

.. toctree::
   :maxdepth: 2

   guide
   py_api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: links.rst

.. Place your references here:

.. _Liu's Homepage: http://people.csail.mit.edu/celiu/OpticalFlow/
