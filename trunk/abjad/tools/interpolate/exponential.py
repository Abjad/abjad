def exponential(y1, y2, mu, exp=1):
   '''Linear interpolation.
      mu is normalized [0, 1].'''

   return (y1 * (1 - mu ** exp) + y2 * mu ** exp)
