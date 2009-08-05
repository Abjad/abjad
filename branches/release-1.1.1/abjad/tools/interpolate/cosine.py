import math


def cosine(y1, y2, mu):
   '''Cosine interpolation.
      mu is normalized [0, 1].'''

   mu2 = (1 - math.cos(mu * math.pi)) / 2
   return (y1 * (1 - mu2) + y2 * mu2)
