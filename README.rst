=================================================
 Python Bindings to Liu's Optical Flow Framework
=================================================

This package is a simple Boost.Python wrapper to the open-source Optical Flow
estimator developed by C. Liu during his Ph.D. The code was originally
conceived to operate over Matlab. This is a Python/Bob port. If you use this
code, the author asks you to cite the following paper::

    @thesis{Liu_PHD_2009,
      title = {{Beyond Pixels: Exploring New Representations and Applications for Motion Analysis}},
      author = {Liu, C.},
      institution = {{Massachusetts Institute of Technology}},
      year = {2009},
      type = {{Ph.D. Thesis}},
    }

If you decide to use this port on your publication, we kindly ask you to cite
Bob as well, as the base software framework, on which this port has been
developed::

    @inproceedings{Anjos_ACMMM_2012,
        author = {A. Anjos AND L. El Shafey AND R. Wallace AND M. G\"unther AND C. McCool AND S. Marcel},
        title = {Bob: a free signal processing and machine learning toolbox for researchers},
        year = {2012},
        month = oct,
        booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
        publisher = {ACM Press},
    }

`Here is a link <http://people.csail.mit.edu/celiu/OpticalFlow/>`_ to Liu's
homepage with details on the code, also displaying the original Matlab port.

Installation
------------

You can just add a dependence for ``xbob.optflow.liu`` on your ``setup.py`` to
automatically download and have this package available at your satellite
package. This works well if Bob is installed centrally at your machine. 

Otherwise, you will need to tell ``buildout`` how to build the package locally
and how to find Bob. For that, just add a custom egg recipe to your
buildout that will fetch the package and compile it locally, setting the
environment variable ``PKG_CONFIG_PATH`` to where Bob is installed. For
example::

  [buildout]
  parts = xbob.optflow.liu <other parts here...>
  ...

  [env]
  PKG_CONFIG_PATH = /Users/andre/work/bob/build/install/lib/pkgconfig

  ...

  [xbob.optflow.liu]
  recipe = zc.recipe.egg:custom
  environment = env

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
  from xbob.optflow.liu import flow
  ...
  (u, v, warped) = flow(image1, image2)

The ``flow`` method accepts more parameters. Please refer to its built-in
documentation for details.
