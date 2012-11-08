from . import _flandmark

from pkg_resources import resource_filename

def __filename__(f):
  """Returns the test file on the "data" subdirectory"""
  return resource_filename(__name__, f)

class Localizer(_flandmark.Localizer):
  """A fast and effective facial landmark localization framework based on
  flandmark
  
  Consult http://cmp.felk.cvut.cz/~uricamic/flandmark/index.php for more
  information.
  """

  def __init__(self, detection_model=resource_filename(__name__, 
    'haarcascade_frontalface_alt.xml'),
    localization_model=resource_filename(__name__,
      'flandmark_model.dat')):
    """Builds a new facial localization model.

    Raises RuntimeError's if the models either don't exist or can't be loaded.

    Keyword parameters:

    detection_model
      An OpenCV (xml) detection model file for a CvHaarClassifierCascade. If not
      specified, use a default installed with the package.

    localization_model
      A flandmark localization model file. If not specified, use a default
      installed with the package. The default model provides the following
      keypoints, in this order:

      [0]
        Face center

      [1]
        Canthus-rl (inner corner of the right eye). Note: The "right eye" means
        the right eye at face w.r.t. itself - that is the left eye in the image.

      [2]
        Canthus-lr (inner corder of the left eye)

      [3]
        Mouth-corner-r (right corner of the mouth)

      [4]
        Mouth-corner-l (left corner of the mouth)

      [5]
        Canthus-rr (outer corner of the right eye)

      [6]
        Canthus-ll (outer corner of the left eye)

      [7]
        Nose
    """
    super(Localizer, self).__init__(detection_model, localization_model)

  def __call__(self, image):
    """Localizes facial keypoints on all faces detected at the input image.

    Keyword parameters:

    image
      Either a gray-scale or colored image where to run the detection and
      localization.

    Returns a tuple composed of dictionaries. Each dictionary in the list has
    two entries: ``bbox`` and ``landmark``. The ``bbox`` entry corresponds to
    the OpenCV cascade face detected, whereas the ``landmark`` contains a list
    of tuples (representing x,y coordinates) with the landmarks.

    If no faces are detected on the input image, than the returned tuple is
    empty.
    """

    if image.ndim == 3:
      from bob.ip import rgb_to_gray
      gray = rgb_to_gray(image)
      return super(Localizer, self).__call__(gray)

    elif image.ndim == 2:
      return super(Localizer, self).__call__(gray)

    else:
      raise TypeError, "Localizer accepts images as numpy.ndarray objects with either 2 or 3 dimensions"
