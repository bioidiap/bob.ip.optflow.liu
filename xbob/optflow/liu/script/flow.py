#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Fri 21 Sep 2012 10:43:12 CEST 

"""Annotates videos, dumps annotations as text files.

The text files will contain one line per annotated frame. Each line contains a
single detected face and associated landmarks. Only the biggest detection found
on the frame is considered. The entries in each line are:

[0]
  The frame number (starting from 0)

[1:5] 4 items
  The bounding-box coordinates as detected by OpenCV (x, y, width, height)

[5:] 8 pairs
  Each pair corresponds to a keypoint in the order defined by the model:

  [5:7]
    Face center (as defined by the OpenCV detected bounding box)

  [7:9]
    Canthus-rl (inner corner of the right eye). Note: The "right eye" means
    the right eye at face w.r.t. itself - that is the left eye in the image.

  [9:11]
    Canthus-lr (inner corder of the left eye)

  [11:13]
    Mouth-corner-r (right corner of the mouth)

  [13:15]
    Mouth-corner-l (left corner of the mouth)

  [15:17]
    Canthus-rr (outer corner of the right eye)

  [17:19]
    Canthus-ll (outer corner of the left eye)

  [19:21]
    Nose

If no faces are found on the frame, the line will only display an invalid
bounding box with zeros, e.g. `327 0 0 0 0`. No landmarks will be displayed in
this case.
"""

import os
import sys
import bob
from .. import Localizer
import pkg_resources

def get_biggest(dets):
  """Returns the biggest detection found"""
  retval = dets[0]
  for d in dets[1:]:
    if retval['bbox'][2] < d['bbox'][2]: retval = d
  return retval

def main():

  import argparse

  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('video', metavar='VIDEO', type=str,
      help="Video file to load")

  parser.add_argument('output', metavar='OUTPUT', type=str,
      default=None, nargs='?',
      help="If you prefer the output diverged to a file, enter this argument")

  parser.add_argument('-v', '--verbose', default=False, action='store_true',
      help="Increases the output verbosity level")

  from ..version import __version__
  name = os.path.basename(os.path.splitext(sys.argv[0])[0])
  parser.add_argument('-V', '--version', action='version',
      version='Automatic Video Keypoint Annotation Tool v%s (%s)' % (__version__, name))

  args = parser.parse_args()

  if not os.path.exists(args.video):
    parser.error("Input video file '%s' cannot be read" % args.video)

  output = sys.stdout

  if args.output is not None:
    dirname = os.path.dirname(args.output)

    if dirname and not os.path.exists(dirname):
      try:
        os.makedirs(dirname)
      except OSError as exc:
        import errno
        if exc.errno == errno.EEXIST: pass
        else: raise

    output = open(args.output, 'wt')

  op = Localizer()
  v = bob.io.VideoReader(args.video)
  if args.verbose and args.output is not None:
    print "Locating faces in %d frames" % len(v),
  for k, frame in enumerate(v):
    dets = op(frame)
    if dets:
      biggest = get_biggest(dets)
      bbox = biggest['bbox']
      landmarks = biggest['landmark']
      output.write("%d %d %d %d %d " % ((k,) + bbox))
      lstr = " ".join("%d %d" % (round(p[0]), round(p[1])) for p in landmarks)
      output.write(lstr + "\n")
      if args.verbose and args.output is not None:
        sys.stdout.write('.')
        sys.stdout.flush()

    else:
      output.write("%d 0 0 0 0\n" % k)
      if args.verbose and args.output is not None:
        sys.stdout.write('x')
        sys.stdout.flush()
    
  if args.verbose and args.output is not None:
    sys.stdout.write('\n')
    sys.stdout.flush()
