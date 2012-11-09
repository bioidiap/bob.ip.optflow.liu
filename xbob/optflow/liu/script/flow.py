#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Fri 21 Sep 2012 10:43:12 CEST 

"""Estimates the optical flow between images or in a video

This program will dump a single output HDF5 file that contains a 3D double
array with two planes. Each plane matches the size of the image or video input.
The first plane corresponds to the output of the flow estimation along the
horizontal axis, i.e. the horizontal velocities, also known as Vx or U in many
papers. The second plane corresponds to the vertical velocities, also know as
Vy or V.

The input may be composed of a single input video or an image sequence. In case
the input is composed of a set of input images, the images **must** be of the
same size. The output is an HDF5 file that contains the flow estimations
between every 2 consecutive images in the input data.
"""

__epilog__ = """Usage Example:

1. Estimate the OF in a video:

  $ %(prog)s myvideo.avi myflow.hdf5

2. Estimate the OF in an image sequence:

  $ %(prog)s image1.jpg image2.jpg flow.hdf5
"""

import os
import sys
import bob

def load_and_grayscale_images(l):
  """Loads and grayscales all input images in the list
  """

  retval = [bob.io.load(k) for k in l]
  for i, k in enumerate(retval):
    if k.ndim == 3: retval[i] = bob.ip.rgb_to_gray(k)
    elif k.ndim != 2:
      raise RuntimeError, "Input image file `%s' does not have 2 or 3 planes in first dimension - is it an image at all?" % l[i]

  return retval

def main():

  import argparse

  parser = argparse.ArgumentParser(description=__doc__, epilog=__epilog__,
      formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('input', metavar='INPUT', type=str, nargs='+',
      help="Input file(s) to load")

  parser.add_argument('output', metavar='OUTPUT', type=str, 
      help="Where to place the output")

  parser.add_argument('-v', '--verbose', default=False, action='store_true',
      help="Increases the output verbosity level")

  from ..version import __version__
  name = os.path.basename(os.path.splitext(sys.argv[0])[0])
  parser.add_argument('-V', '--version', action='version',
      version='Optical Flow Estimation Tool v%s (%s)' % (__version__, name))

  args = parser.parse_args()

  for i in args.input:
    if not os.path.exists(i):
      parser.error("Input file '%s' cannot be read" % i)

  dirname = os.path.dirname(args.output)

  if dirname and not os.path.exists(dirname):
    try:
      os.makedirs(dirname)
    except OSError as exc:
      import errno
      if exc.errno == errno.EEXIST: pass
      else: raise

  from .. import flow

  flows = []
  if len(args.input) == 1: #assume this is a video sequence

    pass

  else: #assume the user has given us N images

    # gray scale every one
    input = load_and_grayscale_images(args.input)

    for index, (i1, i2) in enumerate(zip(input[:-1], input[1:])):
      if args.verbose:
        sys.stdout.write('%s -> %s\n' % tuple(args.input[index:index+2]))
        sys.stdout.flush()
      flows.append(flow(i1, i2)[0:2])

  if args.verbose:
    sys.stdout.write('Saving flows to %s\n' % args.output)
    sys.stdout.flush()

  bob.io.save(flows, args.output)
