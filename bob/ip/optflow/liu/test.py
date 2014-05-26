#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Fri 21 Sep 2012 09:19:39 CEST

"""Tests for Liu's Optical Flow estimation python bindings
"""

import os
import numpy
import nose.tools
import pkg_resources

import bob.io.base
import bob.io.image
import bob.io.video

from . import cg, sor

def F(name, f):
  """Returns the test file on the "data" subdirectory"""
  return pkg_resources.resource_filename(name, os.path.join('data', f))

INPUT_VIDEO = F('bob.io.video', 'test.mov')

def run_for(sample, method):

  refdir = sample.split(os.sep)
  refdir.insert(1, method)
  refdir = os.sep.join(refdir)

  f = bob.io.base.HDF5File(F(__name__, refdir + '.hdf5'))
  method = sor.flow if method == 'sor' else cg.flow

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

  i1 = bob.io.base.load(F(__name__, '%s1.png' % sample)).astype('float64')/255.
  i2 = bob.io.base.load(F(__name__, '%s2.png' % sample)).astype('float64')/255.

  (u, v, wi2) = method(i1, i2, alpha, ratio, min_width,
      n_outer_fp_iterations, n_inner_fp_iterations, n_iterations)

  if __import__('platform').architecture()[0] == '32bit':
    #not as precise
    assert numpy.allclose(uv[0,:,:], u, atol=1e-1)
    assert numpy.allclose(uv[1,:,:], v, atol=1e-1)
  else:
    #full precision
    assert numpy.allclose(uv[0,:,:], u)
    assert numpy.allclose(uv[1,:,:], v)

@nose.tools.nottest
def test_car_gray_SOR():
  run_for('gray/car', 'sor')

def test_table_gray_SOR():
  run_for('gray/table', 'sor')

def test_table_gray_CG():
  run_for('gray/table', 'cg')

@nose.tools.nottest
def test_simple_gray_SOR():
  run_for('gray/simple', 'sor')

@nose.tools.nottest
def test_complex_gray_SOR():
  run_for('gray/complex', 'sor')

# Note: color + SOR not working for the time being. Ce Liu notified -
# 13.11.2012
def test_car_color_CG():
  run_for('color/car', 'cg')

def external_run(sample, method):
  from .script import flow

  # prepare temporary file
  import tempfile
  (fd, out) = tempfile.mkstemp('.hdf5')
  os.close(fd)
  del fd
  os.unlink(out)

  try:
    refdir = sample.split(os.sep)
    refdir.insert(1, method)
    refdir = os.sep.join(refdir)

    f = bob.io.base.HDF5File(F(__name__, refdir + '.hdf5'))

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
    nose.tools.eq_(flow.main(args), 0)

    #load and check
    uvref = f.read('uv')
    uv = bob.io.base.load(out)
    if __import__('platform').architecture()[0] == '32bit':
      #not as precise
      assert numpy.allclose(uvref, uv, atol=1e-1)
    else:
      #full precision
      assert numpy.allclose(uvref, uv)

  finally:
    if os.path.exists(out): os.unlink(out)

def test_table_gray_sor_script():
  external_run('gray/table', 'sor')

# Note: color + SOR not working for the time being. Ce Liu notified -
# 13.11.2012
@nose.tools.nottest
def test_table_color_sor_script():
  external_run('gray/table', 'sor')

@nose.tools.nottest
def test_simple_gray_cg_script():
  external_run('gray/simple', 'cg')

@nose.tools.nottest
def test_rubberwhale_color_cg_script():
  external_run('color/rubberwhale', 'cg')

@nose.tools.nottest
def test_video_script():
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
    nose.tools.eq_(flow.main(args), 0)

    #load and check
    uv = bob.io.base.load(out)
    nose.tools.eq_( len(uv), N-1 )

  finally:
    assert os.path.exists(out)
    os.unlink(out)
