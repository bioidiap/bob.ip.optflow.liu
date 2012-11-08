#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Fri 21 Sep 2012 10:47:05 CEST 

"""Returns the currently compiled version number"""

__version__ = __import__('pkg_resources').get_distribution('flandmark').version
