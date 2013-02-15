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
from . import sor_flow, cg_flow

def F(name, f):
  """Returns the test file on the "data" subdirectory"""
  return pkg_resources.resource_filename(name, os.path.join('data', f))

INPUT_VIDEO = F('bob.io.test', 'test.mov')

class OpticalFlowLiuTest(unittest.TestCase):
  """Performs various tests on Ce Liu's Optical Flow package"""

  def run_for(self, sample, refdir):

    f = bob.io.HDF5File(os.path.join(refdir, '%s.hdf5' % sample))
    method = sor_flow if f.get_attribute('method', 'uv') == 'SOR' else cg_flow

    # the reference flow field to use
    uv = f.read('uv')

    # the values of parameters used for this flow field estimation
    alpha = f.get_attribute('alpha', 'uv')
    ratio = f.get_attribute('ratio', 'uv')
    min_width = int(f.get_attribute('min_width', 'uv'))
    n_inner_fp_iterations = int(f.get_attribute('n_inner_fp_iterations', 'uv'))
    n_outer_fp_iterations = int(f.get_attribute('n_outer_fp_iterations', 'uv'))

    if f.has_attribute('n_sor_iterations', 'uv'):
      n_iterations = int(f.get_attribute('n_sor_iterations', 'uv'))
    elif f.has_attribute('n_cg_iterations', 'uv'):
      n_iterations = int(f.get_attribute('n_cg_iterations', 'uv'))
    else:
      n_iterations = int(f.get_attribute('n_iterations', 'uv'))

    i1 = bob.io.load(F(__name__, '%s1.png' % sample)).astype('float64')/255.
    i2 = bob.io.load(F(__name__, '%s2.png' % sample)).astype('float64')/255.

    (u, v, wi2) = method(i1, i2, alpha, ratio, min_width,
        n_outer_fp_iterations, n_inner_fp_iterations, n_iterations)

    self.assertTrue( numpy.allclose(uv[0,:,:], u) )
    self.assertTrue( numpy.allclose(uv[1,:,:], v) )

  def test01_car_gray_SOR(self):
    self.run_for('gray/car', 'reference/sor_based')

  def test02_table_gray_SOR(self):
    self.run_for('gray/table', 'reference/sor_based')

  def test03_table_gray_CG(self):
    self.run_for('gray/table', 'reference/cg_based')

  def test04_simple_gray_SOR(self):
    self.run_for('gray/simple', 'reference/sor_based')

  def test05_complex_gray_SOR(self):
    self.run_for('gray/complex', 'reference/sor_based')

  # Note: color + SOR not working for the time being. Ce Liu notified -
  # 13.11.2012

  def test06_car_color_CG(self):
    self.run_for('color/car', 'reference/cg_based')

  def external_run(self, sample, refdir):
    from .script import flow
   
    # prepare temporary file
    import tempfile
    (fd, out) = tempfile.mkstemp('.hdf5')
    os.close(fd)
    del fd
    os.unlink(out)

    try:
      f = bob.io.HDF5File(os.path.join(refdir, sample + '.hdf5'))
 
      # the values of parameters used for this flow field estimation
      alpha = f.get_attribute('alpha', 'uv')
      ratio = f.get_attribute('ratio', 'uv')
      min_width = int(f.get_attribute('min_width', 'uv'))
      n_outer_fp_iterations = int(f.get_attribute('n_outer_fp_iterations', 'uv'))
      n_inner_fp_iterations = int(f.get_attribute('n_inner_fp_iterations', 'uv'))

      if f.has_attribute('n_sor_iterations', 'uv'):
        n_iterations = int(f.get_attribute('n_sor_iterations', 'uv'))
      elif f.has_attribute('n_cg_iterations', 'uv'):
        n_iterations = int(f.get_attribute('n_cg_iterations', 'uv'))
      else:
        n_iterations = int(f.get_attribute('n_iterations', 'uv'))

      args = ['--verbose', f.get_attribute('method', 'uv').lower()]
      args += [
          '--alpha=%f' % alpha,
          '--ratio=%f' % ratio,
          '--min-width=%d' % min_width,
          '--outer-fp-iterations=%d' % n_outer_fp_iterations,
          '--inner-fp-iterations=%d' % n_inner_fp_iterations,
          '--iterations=%d' % n_iterations,
          ]

      args.append(F(__name__, '%s1.png' % sample))
      args.append(F(__name__, '%s2.png' % sample))
      args.append(out)
      self.assertEqual(flow.main(args), 0)

      #load and check
      uvref = f.read('uv')
      uv = bob.io.load(out)
      self.assertTrue( numpy.allclose(uvref, uv) )

    finally:
      if os.path.exists(out): os.unlink(out)

  def test07_car_gray_sor_script(self):
    self.external_run('gray/complex', 'reference/sor_based')

  # Note: color + SOR not working for the time being. Ce Liu notified -
  # 13.11.2012
  def xtest08_table_color_sor_script(self):
    self.external_run('gray/table', 'reference/sor_based')

  def test09_simple_gray_cg_script(self):
    self.external_run('gray/simple', 'reference/cg_based')

  def test10_rubberwhale_color_cg_script(self):
    self.external_run('color/rubberwhale', 'reference/cg_based')

  def test11_video_script(self):
    from .script import flow
    import tempfile
    N = 3
   
    try:
      args = ['--verbose', '--video-frames=%d' % N, 'sor']
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
