def linear(y1, y2, mu):
   '''Linear interpolation.
      mu is normalized [0, 1].
   '''

   return (y1 * (1 - mu) + y2 * mu)
