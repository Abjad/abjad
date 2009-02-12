import math

def interpolate_cosine(y1, y2, mu):
   '''
   Cosine interpolation.
   mu is normalized [0, 1].
   '''
   mu2 = (1 - math.cos(mu * math.pi)) / 2
   return (y1 * (1 - mu2) + y2 * mu2)


def interpolate_linear(y1, y2, mu):
   '''
   Linear interpolation.
   mu is normalized [0, 1].
   '''
   return (y1 * (1 - mu) + y2 * mu)


def interpolate_exponential(y1, y2, mu, exp=1):
   '''
   Linear interpolation.
   mu is normalized [0, 1].
   '''
   return (y1 * (1 - mu ** exp) + y2 * mu ** exp)


