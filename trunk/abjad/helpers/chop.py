def chop(x):
   '''Return the integer part of x.'''

   if x >= 0:
      return int(x)
   else:
      return -int(abs(x))
