#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Fri 21 Sep 2012 09:19:39 CEST 

"""Tests for Liu's Optical Flow estimation python bindings
"""

import os, sys
import unittest
import bob
import numpy
import pkg_resources
from . import flow, grayscale_double

EXAMPLES = 'example'
EXAMPLE_URL = 'https://github.com/downloads/bioidiap/xbob.optflow.liu/example-v1.zip'

def F(name, f):
  """Returns the test file on the "data" subdirectory"""
  return pkg_resources.resource_filename(name, os.path.join('data', f))

INPUT_VIDEO = F('bob.io.test', 'test.mov')

class OpticalFlowLiuTest(unittest.TestCase):
  """Performs various tests on Ce Liu's Optical Flow package"""

  def setUp(self):
    """Download/check example files"""

    if not os.path.exists(EXAMPLES):
      print "Get `%s'..." % EXAMPLE_URL
      import urllib, zipfile, cStringIO
      zfile = zipfile.ZipFile(cStringIO.StringIO(urllib.urlopen(EXAMPLE_URL).read()))
      print "Extract `%s'..." % os.path.basename(EXAMPLE_URL)
      for name in zfile.namelist():
        if name[-1] == os.sep:
          if not os.path.exists(name): os.mkdir(name)
        else:
          fd = open(name, 'w')
          fd.write(zfile.read(name))
          fd.close()
      print "All done, setup Ok."

  def run_for(self, sample):

    f = bob.io.HDF5File(os.path.join(EXAMPLES, '%s.hdf5' % sample))

    # the reference flow field to use
    uv = f.read('uv')

    # the values of parameters used for this flow field estimation
    alpha = f.get_attribute('alpha', 'uv')
    ratio = f.get_attribute('ratio', 'uv')
    min_width = int(f.get_attribute('min_width', 'uv'))
    n_inner_fp_iterations = int(f.get_attribute('n_inner_fp_iterations', 'uv'))
    n_outer_fp_iterations = int(f.get_attribute('n_outer_fp_iterations', 'uv'))
    n_sor_iterations = int(f.get_attribute('n_sor_iterations', 'uv'))

    i1 = grayscale_double(bob.io.load(os.path.join(EXAMPLES, '%s1.png' % sample)))
    i2 = grayscale_double(bob.io.load(os.path.join(EXAMPLES, '%s2.png' % sample)))

    (u, v, wi2) = flow(i1, i2, alpha, ratio, min_width,
        n_outer_fp_iterations, n_inner_fp_iterations, n_sor_iterations)

    self.assertTrue( numpy.array_equal(uv[0,:,:], u) )
    self.assertTrue( numpy.array_equal(uv[1,:,:], v) )

  def test01_car(self):
    self.run_for('car')

  def test02_table(self):
    self.run_for('table')

  def test03_simple(self):
    self.run_for('simple')

  def test04_complex(self):
    self.run_for('complex')

  def external_run(self, sample):
    from .script import flow
    import tempfile
   
    try:
      args = ['--verbose']
      args.append(os.path.join(EXAMPLES, '%s1.png') % sample)
      args.append(os.path.join(EXAMPLES, '%s2.png') % sample)
      (fd, out) = tempfile.mkstemp('.hdf5')
      os.close(fd)
      del fd
      os.unlink(out)
      args.append(out)
      self.assertEqual(flow.main(args), 0)

      #load and check
      uvref = bob.io.load(os.path.join(EXAMPLES, '%s.hdf5') % sample)
      uv = bob.io.load(out)
      self.assertTrue( numpy.array_equal(uvref, uv) )

    finally:
      self.assertTrue(os.path.exists(out))
      os.unlink(out)

  def test05_car_script(self):
    self.external_run('car')

  def test06_video_script(self):
    from .script import flow
    import tempfile
    N = 3
   
    try:
      args = ['--verbose', '--video-frames=%d' % N]
      args.append(INPUT_VIDEO)
      (fd, out) = tempfile.mkstemp('.hdf5')
      os.close(fd)
      del fd
      os.unlink(out)
      args.append(out)
      self.assertEqual(flow.main(args), 0)

      #load and check
      uv = bob.io.load(out)
      self.assertEqual( len(uv), N-1 )

    finally:
      self.assertTrue(os.path.exists(out))
      os.unlink(out)
