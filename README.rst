=================================================
 Python Bindings to Liu's Optical Flow Framework
=================================================

This package is a simple Boost.Python wrapper to the open-source Optical Flow
estimator developed by C. Liu during his Ph.D. The code was originally
conceived to operate over Matlab. This is a Python/`Bob
<http://www.idiap.ch/software/bob/>`_ port. If you use this code, the author
asks you to cite the following paper::

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

`Here is a link <http://people.csail.mit.edu/celiu/OpticalFlow/>`_ to Liu's
homepage with details on the code, also displaying the original Matlab port.

Installation
------------

You can just add a dependence for ``xbob.optflow.liu`` on your ``setup.py`` to
automatically download and have this package available at your satellite
package. This works well if Bob is installed centrally at your machine.

Otherwise, you will need to tell ``buildout`` how to build the package locally
and how to find Bob. For that, just add a recipe to your buildout that will
fetch the package and compile it locally, setting the buildout variable
``prefixes`` to where Bob is installed (a build directory will also work). For
example::

  [buildout]
  parts = xbob.optflow.liu <other parts here...>
  prefixes = /Users/andre/work/bob/build/debug
  ...

  [xbob.optflow.liu]
  recipe = xbob.buildout:develop

  ...

Development
-----------

To develop these bindings, you will need the open-source library `Bob
<http://www.idiap.ch/software/bob/>`_ installed somewhere. At least version
1.1.0 of Bob is required. If you have compiled Bob yourself and installed it on
a non-standard location, you will need to note down the path leading to the
root of that installation.

Just type::

  $ python bootstrap.py
  $ ./bin/buildout

If Bob is installed in a non-standard location, edit the file ``buildout.cfg``
to set the root to Bob's local installation path. Remember to use the **same
python interpreter** that was used to compile Bob, then execute the same steps
as above.

Usage
-----

Pretty simple, just do something like::

  import bob
  from xbob.optflow.liu import cg_flow as flow
  ...
  (u, v, warped) = flow(image1, image2)

The ``cg_flow`` method accepts more parameters. Please refer to its built-in
documentation for details.

Reproducible Research Notes
---------------------------

Some notes on being able to reproduce consistent results through the different
platforms supported by `Bob`_.

Differences between Matlab and Bob/Python ports
===============================================

I have detected inconsistencies between output produced by these pythonic
bindings and Ce Liu's Matlab-based implementation. In all instances, these
differences come from differences in either the gray-scaling conversion and/or
the decompression routines for the test images and movies. Once a precise input
is given in double-precision gray-scale, both bindings (ours and Ce Liu's
Matlab ones) give out **exactly** the same output.

This means that you should expect precision problems if you feed in videos or
lossy input formats such as JPEG images. If you input HDF5 files, Matlab
``.mat`` files or any other data in formats which are **not** subject to lossy
compression/decompression, this data is pre-grayscaled **and** stored in
double-precision floating point numbers, the output is consistently the same,
no matter which environment you use.

If you input data which is not double-precision gray-scale, then it is (1)
converted to double-precision representation and then (2) gray-scaled. These
steps are taken in this order in both bindings. Depending on which you are
using (Bob/Python *versus* Matlab), the results will be slightly different.
This small differences in the input to the flow estimation engine will make
Liu's framework give (hopefully slightly) different output. The outputs should
be comparable though, but your mileage may vary.

New SOR-based Implementation
============================

More recently (in August 2011), Ce Liu introduced a version of the Optical
Flow framework using Successive Over-Relaxation (SOR) instead of Conjugate
Gradient (CG) for minization. The new framework is presumably faster, but
does not give similar results compared to the old CG-based one.

If you would like to give it a spin, use the method ``sor_flow`` instead of
``cg_flow`` as shown above. Notice that the defaults for both implementations
are different, following the defaults pre-set in the Matlab MEX code in the
different releases.

Particularly, avoid feeding colored images to ``sor_flow``. While that works
OK with ``cg_flow``, ``sor_flow`` gives inconsistent results everytime it is
run. I recommend gray-scaling images before using ``sor_flow``. With that,
results are at least consistent between runs. I'm not sure about their
correctness. Ce Liu has been informed and should be working on it soon
enough (today is 14.Nov.2012).

To access this implementation, use `xbob.optflow.liu.sor_flow`.

Access to the MATLAB code
=========================

Once you have installed the package, you will have access to a directory called
``matlab``, which contains the code as it is/was distributed by Ce Liu, and a
few Matlab routines that can be used to produce samples for testing. To use the
Matlab code, you must::

  $ # matlab/cg_based  => CG-based implementation
  $ # matlab/sor_based => SOR-based implementation
  $ cd matlab/cg_based/mex
  $ mex Coarse2FineTwoFrames.cpp OpticalFlow.cpp GaussianPyramid.cpp
  $ cd ..

At this point, the MEX is compiled and ready to be used. You will find 2
routines on the directory: ``flowimage`` and ``flowmovie``. They can be used to
process single images or movie files. They both produce `HDF5
<http://www.hdfgroup.org/HDF5/>`_ files that can be used as test input for this
package's test suite, or for inspection (use ``h5dump`` to look into the file
contents).

Here is an example of usage for the Matlab function ``flowimage``::

  $ matlab
  ...
  >> flowimage ../../xbob/optflow/liu/data/gray table .

This will generate a file called ``table.hdf5`` that contains the flow
calculated for the ``table`` example, i.e. between images ``table1.png`` and
``table2.png``. The input images are pre-gray-scaled and are taken from
the directory ``../../xbob/optflow/liu/data/gray``, following your command.

You will find more examples on this directory and on the 
``../../xbob/optflow/liu/data/gray`` directory.

.. note::

  The contents of the directory ``reference`` are downloaded automatically by
  buildout. You can find the URL of the package by looking inside the file
  ``buildout.cfg``.

.. note::

  The example images are coded in PNG format so that they don't suffer from
  compression/decompression problems and can be read the same way in any
  platform or implementation.
