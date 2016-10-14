.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Thu  3 Apr 13:47:28 2014 CEST
..
.. Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland

==============
 User's Guide
==============

There are two versions of the Optical Flow framework implemented on this
package. A older version, based on Conjugate-Gradient (CG) for minization and a
newer version, based on Successive-Over-Relaxation (SOR). Both versions accept
input images in either gray-scale (2D arrays with shape ``(height, width)``) or
colored (3D arrays with shape ``(3, height, width)``). The data type of the
arrays can be any, but if different than ``float64``, an internal casting will
take place. Similarly, RGB images will be gray-scaled before usage. For
efficience, it is recommended only 2D arrays with 64-bit floats are passed as
input.

To use the CG-based implementation, do this:

.. code-block:: py

   >>> import bob.ip.optflow.liu
   ...
   >>> (u, v, warped) = bob.ip.optflow.liu.cg.flow(image1, image2)

.. note::
   The :py:func:`bob.ip.optflow.liu.cg.flow` method accepts more parameters.

Optionally, you can also use the new SOR-based implementation included in the package.
To do so, do the following instead:

.. code-block:: py

   >>> import bob.ip.optflow.liu
   ...
   (u, v, warped) = bob.ip.optflow.liu.sor.flow(image1, image2)

.. warning::

   If you'd like to feed colored images into :py:func:`bob.ip.optflow.liu.sor.flow`, make sure to read and understand our :ref:`rr-note` below.

.. _rr-note:

Reproducible Research Notes
---------------------------

In order to be able to test (and attest) the correct functioning of this port, a set of unit tests were implemented.
These tests are based on image pairs available on Liu's website (car, table, etc.).
For each pair and explored conditions, a Matlab reference for the computed flow was produced and recorded into :py:class:`bob.io.base.HDF5File` files.
The files are used to compare the results of the flow calculated by these bindings, using the same input parameters and image pairs.

This section contains notes for tests executed in different architectures or using different options and implementations.

.. note::

   The Matlab references were produced in a 64-bit machine running Linux.

Architecture Imprecisions
=========================
While running the unit tests, I can verify that our (64-bit) references check against values produced by these bindings on 64-bit architectures, under Linux or Mac OSX.
In the case this package is compiled and ran on a 32-bit system, the results are not as accurate, because of the reduced precision.
The 64-bit reference values for a set of image pairs can be matched, on a such a system, only with about :math:`0.1` absolute precision.

Tests against a 64-bit build of these bindings do not show any significative differences to an absolute accuracy of :math:`10^{-08}` and a relative accuracy of :math:`10^{-5}`.
Because of effect, we recommend you use a 64-bit machine for estimating your flows.

Differences between Matlab and Bob/Python ports
===============================================

I have detected inconsistencies between output produced by these pythonic bindings and Ce Liu's Matlab-based implementation.
In all instances, these differences come from differences in either the gray-scaling conversion and/or the decompression routines for the test images and movies.
Once a precise input is given in double-precision gray-scale, both bindings (ours and Ce Liu's Matlab ones) give out **exactly** the same output.

This means that you should expect precision problems if you feed in videos or
lossy input formats such as JPEG images.  If you input HDF5 files (e.g. using
:py:mod:`bob.io.base`), Matlab ``.mat`` files (e.g. using
:py:mod:`bob.io.matlab`) or any other data in formats which are **not** subject
to lossy compression/decompression, this data is pre-grayscaled **and** stored
in double-precision floating point numbers, the output is consistently the
same, no matter which environment you use.

If you input data which is not double-precision gray-scale, then it is (1) converted to double-precision representation and then (2) gray-scaled.
These steps are taken in this order in both bindings.
Depending on which you are using (Bob/Python *versus* Matlab), the results will be slightly different.
This small differences in the input to the flow estimation engine will make Liu's framework give (hopefully slightly) different output.
The outputs should be comparable though, but your mileage may vary.

New SOR-based Implementation
============================

More recently (in August 2011), Ce Liu introduced a version of the Optical Flow framework using Successive Over-Relaxation (SOR) instead of Conjugate Gradient (CG) for minization.
The new framework is presumably faster, but does not give similar results compared to the old CG-based one.

If you would like to give it a spin, use the method :py:func:`bob.ip.optflow.liu.sor.flow` instead of py:func:`bob.ip.optflow.liu.cg.flow` as shown above.
Notice that the defaults for both implementations are different, following the defaults pre-set in the Matlab MEX code in the different releases.

Particularly, avoid feeding colored images to
:py:func:`bob.ip.optflow.liu.sor.flow`.  While that works OK with
:py:func:`bob.ip.optflow.liu.cg.flow`, :py:func:`bob.ip.optflow.liu.sor.flow`
gives inconsistent results everytime it is run. I recommend gray-scaling
images before using :py:func:`bob.ip.optflow.liu.sor.flow`, e.g., by
converting them using :py:func:`bob.ip.color.rgb_to_gray`. With that, results
are at least consistent between runs.  I'm not sure about their correctness.
Ce Liu has been informed and should be working on it soon enough (today is
14.Nov.2012).

To access this implementation, use :py:func:`bob.ip.optflow.liu.sor.flow`.

Access to the MATLAB code
=========================

Once you have installed the package, you will have access to a directory called ``matlab``, which contains the code as it is/was distributed by Ce Liu, and a few Matlab routines that can be used to produce samples for testing.
To use the Matlab code, you must:

.. code-block:: sh

  $ # matlab/cg_based  => CG-based implementation
  $ # matlab/sor_based => SOR-based implementation
  $ cd matlab/cg_based/mex
  $ mex Coarse2FineTwoFrames.cpp OpticalFlow.cpp GaussianPyramid.cpp
  $ cd ..

At this point, the MEX is compiled and ready to be used.
You will find 2 routines on the directory: ``flowimage`` and ``flowmovie``.
They can be used to process single images or movie files.
They both produce `HDF5`_ files that can be used as test input for this package's test suite, or for inspection (use ``h5dump`` to look into the file contents).

Here is an example of usage for the Matlab function ``flowimage``:

.. code-block:: sh

  $ matlab -nodisplay -nodesktop -nojvm
  >> flowimage ../../bob/ip/optflow/liu/data/gray table .

This will generate a file called ``table.hdf5`` that contains the flow calculated for the ``table`` example, i.e. between images ``table1.png`` and ``table2.png``.
The input images are pre-gray-scaled and are taken from the directory ``../../bob/ip/optflow/liu/data/gray``, following your command.

You will find more examples on this directory and on the ``../../bob/ip/optflow/liu/data/gray`` directory.

.. note::

  The contents of the directory ``reference`` are downloaded automatically by buildout.
  You can find the URL of the package by looking inside the file ``buildout.cfg``.

.. note::

  The example images are coded in PNG format so that they don't suffer from compression/decompression problems and can be read the same way in any platform or implementation.

.. include:: links.rst

