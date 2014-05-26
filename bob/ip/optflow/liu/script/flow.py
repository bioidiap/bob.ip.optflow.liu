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

__epilog__ = """examples:

1. Estimate the OF in a video using the Successive Over-Relaxation (SOR)
   variant:

  $ %(prog)s sor myvideo.avi myflow.hdf5

2. Estimate the OF in an image sequence using the Conjugate Gradient (CG)
   variant:

  $ %(prog)s cg image1.jpg image2.jpg flow.hdf5

3. Get help for a specific variant (and see defaults for that variant):

  $ %(prog)s sor -h
"""

import os
import sys
import argparse
import bob.io.base
import bob.io.image
import bob.io.video
import bob.ip.color

class AliasedSubParsersAction(argparse._SubParsersAction):
  """Hack taken from https://gist.github.com/471779 to allow aliases in
  argparse for python 2.x (this has been implemented on python 3.2)
  """

  class _AliasedPseudoAction(argparse.Action):
    def __init__(self, name, aliases, help):
      dest = name
      if aliases:
        dest += ' (%s)' % ','.join(aliases)
      sup = super(AliasedSubParsersAction._AliasedPseudoAction, self)
      sup.__init__(option_strings=[], dest=dest, help=help)

  def add_parser(self, name, **kwargs):
    if 'aliases' in kwargs:
      aliases = kwargs['aliases']
      del kwargs['aliases']
    else:
      aliases = []

    parser = super(AliasedSubParsersAction, self).add_parser(name, **kwargs)

    # Make the aliases work.
    for alias in aliases:
      self._name_parser_map[alias] = parser
    # Make the help text reflect them, first removing old help entry.
    if 'help' in kwargs:
      help = kwargs.pop('help')
      self._choices_actions.pop()
      pseudo_action = self._AliasedPseudoAction(name, aliases, help)
      self._choices_actions.append(pseudo_action)

    return parser

def add_options(parser, alpha, ratio, min_width, outer, inner, iterations,
    method, variant):

  if variant.lower() == 'cg':
    parser.add_argument('-g', '--gray-scale', dest='gray', default=False, action='store_true', help="Gray-scales input data before feeding it to the flow estimation. This uses Bob's gray scale conversion instead of the Liu's built-in conversion and may lead to slightly different results.")
  else:
    parser.set_defaults(gray=True)

  parser.add_argument('-a', '--alpha', dest='alpha', default=alpha, type=float, metavar='FLOAT', help="Regularization weight (defaults to %(default)s)")

  parser.add_argument('-r', '--ratio', dest='ratio', default=ratio, type=float, metavar='FLOAT', help="Downsample ratio (defaults to %(default)s)")

  parser.add_argument('-m', '--min-width', dest='min_width',
      default=min_width, type=int, metavar='N', help="Width of the coarsest level (defaults to %(default)s)")

  parser.add_argument('-o', '--outer-fp-iterations', metavar='N', dest='outer', default=outer, type=int, help="The number of outer fixed-point iterations (defaults to %(default)s)")

  parser.add_argument('-i', '--inner-fp-iterations', metavar='N', dest='inner', default=inner, type=int, help="The number of inner fixed-point iterations (defaults to %(default)s)")

  parser.add_argument('-x', '--iterations', metavar='N', dest='iterations', default=iterations, type=int, help="The number of %s (error-minimization) iterations (defaults to %%(default)s)" % variant)

  parser.add_argument('input', metavar='INPUT', type=str, nargs='+',
      help="Input file(s) to load")

  parser.add_argument('output', metavar='OUTPUT', type=str,
      help="Where to place the output")

  parser.set_defaults(flow=method)
  parser.set_defaults(variant=variant)

def main(user_input=None):

  from .. import cg, sor

  parser = argparse.ArgumentParser(description=__doc__, epilog=__epilog__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  # part of the hack to support aliases in subparsers
  parser.register('action', 'parsers', AliasedSubParsersAction)

  parser.add_argument('-v', '--verbose', default=False, action='store_true',
      help="Increases the output verbosity level")

  from ..version import module as __version__
  name = os.path.basename(os.path.splitext(sys.argv[0])[0])
  parser.add_argument('-V', '--version', action='version',
      version='Optical Flow Estimation Tool v%s (%s)' % (__version__, name))

  # secret option to limit the number of video frames to run for (test option)
  parser.add_argument('--video-frames', dest='frames', type=int, help=argparse.SUPPRESS)

  # The variants
  variants_parser = parser.add_subparsers(title='variants', help='Method variants implemented. Note different variants will have different defaults for input parameters following the content available on the original Matlab bindings and demonstrators.')

  sor_based = variants_parser.add_parser('sor', aliases=['new'],
      help='Executes the "newer" variant using Successive Over-Relaxation (SOR) instead of Conjugate Gradient (CG).')
  add_options(sor_based, 1.0, 0.5, 40, 4, 1, 20, sor.flow, 'SOR')

  cg_based = variants_parser.add_parser('cg', aliases=['old'],
      help='Executes the "older" variant using Conjugate Gradient (CG). This was the only available implementation until 11.08.2011 on Ce Liu\'s website.')
  add_options(cg_based, 0.02, 0.75, 30, 20, 1, 50, cg.flow, 'CG')

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

  flows = []
  if len(args.input) == 1: #assume this is a video sequence

    if args.frames:

      if args.verbose:
        sys.stdout.write('Loading only %d frames from %s...' % \
            (args.frames, args.input[0]))
        sys.stdout.flush()
        sys.stdout.write('Ok\n')
        sys.stdout.flush()

      input = bob.io.video.reader(args.input[0])[:args.frames]

    else:

      if args.verbose:
        sys.stdout.write('Loading all frames from %s...' % args.input[0])
        sys.stdout.flush()

      input = bob.io.base.load(args.input[0])

  else: #assume the user passed a sequence of images

    input = [bob.io.base.load(k) for k in args.input]

  if args.verbose:
    sys.stdout.write('Converting %d frames to double...' % len(input))
    sys.stdout.flush()

  input = [k.astype('float64')/255. for k in input]

  if args.verbose:
    sys.stdout.write('Ok\n')
    sys.stdout.flush()

  if args.gray and len(input[0].shape) != 2:

    if args.verbose:
      sys.stdout.write('Converting %d frames to grayscale...' % len(input))
      sys.stdout.flush()

    input = [bob.ip.color.rgb_to_gray(k) for k in input]

    if args.verbose:
      sys.stdout.write('Ok\n')
      sys.stdout.flush()

  if args.verbose:
    sys.stdout.write('Processing %d frames' % len(input))
    sys.stdout.flush()

  for index, (i1, i2) in enumerate(zip(input[:-1], input[1:])):
    if args.verbose:
      sys.stdout.write('.')
      sys.stdout.flush()
    flows.append(args.flow(i1, i2, args.alpha, args.ratio, args.min_width,
      args.outer, args.inner, args.iterations)[0:2])

  if args.verbose:
    sys.stdout.write('\n')
    sys.stdout.flush()

  if args.verbose:
    sys.stdout.write('Saving flows to %s\n' % args.output)
    sys.stdout.flush()

  out = bob.io.base.HDF5File(args.output, 'w')
  out.set('uv', flows)
  out.set_attribute('method', args.variant, 'uv')
  out.set_attribute('alpha', args.alpha, 'uv')
  out.set_attribute('ratio', args.ratio, 'uv')
  out.set_attribute('min_width', args.min_width, 'uv')
  out.set_attribute('n_outer_fp_iterations', args.outer, 'uv')
  out.set_attribute('n_inner_fp_iterations', args.inner, 'uv')
  out.set_attribute('n_iterations', args.iterations, 'uv')

  return 0
