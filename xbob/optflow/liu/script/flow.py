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

If you use the results of this script, please consider citing Liu's thesis and
Bob, as the core framework for this port:

  Ce Liu, Beyond Pixels: Exploring New Representations and Applications for
  Motion Analysis, Massachusetts Institute of Technology, 2009.

  A. Anjos, L. El-Shafey, R. Wallace, M. Guenther, C. McCool and S. Marcel,
  Bob: a free signal processing and machine learning toolbox for researchers,
  20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan}, October,
  2012
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

def main(user_input=None):

  import argparse

  parser = argparse.ArgumentParser(description=__doc__, epilog=__epilog__,
      formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('input', metavar='INPUT', type=str, nargs='+',
      help="Input file(s) to load")

  parser.add_argument('output', metavar='OUTPUT', type=str, 
      help="Where to place the output")

  parser.add_argument('-v', '--verbose', default=False, action='store_true',
      help="Increases the output verbosity level")

  parser.add_argument('-a', '--alpha', dest='alpha', default=1.0, type=float, metavar='FLOAT', help="Regularization weight (defaults to %(default)s)")

  parser.add_argument('-r', '--ratio', dest='ratio', default=0.5, type=float, metavar='FLOAT', help="Downsample ratio (defaults to %(default)s)")

  parser.add_argument('-m', '--min-width', dest='min_width', default=40, 
      type=int, metavar='N', help="Width of the coarsest level (defaults to %(default)s)")

  parser.add_argument('-o', '--outer-fp-iterations', metavar='N', dest='outer', default=4, type=int, help="The number of outer fixed-point iterations (defaults to %(default)s)")

  parser.add_argument('-i', '--inner-fp-iterations', metavar='N', dest='inner', default=1, type=int, help="The number of inner fixed-point iterations (defaults to %(default)s)")

  parser.add_argument('-s', '--sor-iterations', metavar='N', dest='sor', default=20, type=int, help="The number of SOR iterations (defaults to %(default)s)")

  from ..version import __version__
  name = os.path.basename(os.path.splitext(sys.argv[0])[0])
  parser.add_argument('-V', '--version', action='version',
      version='Optical Flow Estimation Tool v%s (%s)' % (__version__, name))

  # secret option to limit the number of video frames to run for (test option)
  parser.add_argument('--video-frames', dest='frames', type=int, help=argparse.SUPPRESS)

  args = parser.parse_args(args=user_input)

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

  from .. import flow, grayscale_double

  flows = []
  if len(args.input) == 1: #assume this is a video sequence

    if args.frames:

      if args.verbose:
        sys.stdout.write('Loading only %d frames from %s...' % \
            (args.frames, args.input[0]))
        sys.stdout.flush()

      input = [grayscale_double(k) for k in
          bob.io.VideoReader(args.input[0])[:args.frames]]

    else:

      if args.verbose:
        sys.stdout.write('Loading all frames from %s...' % args.input[0])
        sys.stdout.flush()

      input = [grayscale_double(k) for k in bob.io.load(args.input[0])]

    for index, (i1, i2) in enumerate(zip(input[:-1], input[1:])):
      if args.verbose:
        sys.stdout.write('.')
        sys.stdout.flush()
      flows.append(flow(i1, i2, args.alpha, args.ratio, args.min_width,
        args.outer, args.inner, args.sor)[0:2])

    if args.verbose:
      sys.stdout.write('\n')
      sys.stdout.flush()

  else: #assume the user has given us N images

    # gray scale every one
    input = [grayscale_double(bob.io.load(k)) for k in args.input]

    for index, (i1, i2) in enumerate(zip(input[:-1], input[1:])):
      if args.verbose:
        sys.stdout.write('%s -> %s\n' % tuple(args.input[index:index+2]))
        sys.stdout.flush()
      flows.append(flow(i1, i2, args.alpha, args.ratio, args.min_width,
        args.outer, args.inner, args.sor)[0:2])

    if len(input) == 2: #special case, dump simple
      flows = flows[0]

  if args.verbose:
    sys.stdout.write('Saving flows to %s\n' % args.output)
    sys.stdout.flush()

  bob.io.save(flows, args.output)

  return 0
