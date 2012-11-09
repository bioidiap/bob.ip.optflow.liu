from ._liu import flow

def grayscale_double(a):
  """Grayscales and prepares the input array to be treated by the Optical Flow
  estimation.
  """
  from bob.core import convert
  from bob.ip import rgb_to_gray

  if a.ndim == 3: a = rgb_to_gray(a)
  return a.astype('float64')/255.
