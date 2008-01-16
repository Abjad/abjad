from rational import Rational
from math import log, floor

class Duration(Rational):

   def __init__(self, *args):
      Rational.__init__(self, *args)
      assert self >= 0

   ### REPR ###

   def __repr__(self):
      return 'Duration(%s, %s)' % self.pair

   ### PREDICATES ###
         
   def isBinary(self):
      return not self._d & (self._d - 1)

   def isProper(self):
      return 0 < self < 2
   
   def isTied(self):
      return '01' in self.digits

   def isNoteHeadAssignable(self):
      return self.isBinary( ) and self.isProper( ) and not self.isTied( )

   ### PROPERTIES ###

   @property
   def digits(self):
      result = ''
      n = self._n
      while n > 0:
         result = str(n % 2) + result
         n = n >> 1
      return result

   @property
   def number(self):
      if self.isNoteHeadAssignable( ):
         return 2 ** (int(log(self._d, 2)) - self.dots)
      else:
         return None

   @property
   def dots(self):
      if self.isNoteHeadAssignable( ):
         return sum([int(x) for x in list(self.digits)]) - 1
      else:
         return None

   @property
   def flags(self):
      if self.isNoteHeadAssignable( ):
         return max(-int(floor(log(float(self._n) / self._d, 2))) - 2, 0)
      else:
         return None

   ### FORMATTING ###

   @property
   def lily(self):
      if self.isNoteHeadAssignable( ):
         return '%s%s' % (self.number, '.' * self.dots)
      else:
         raise ValueError('Duration %s can not format as LilyPond input.' %
            self)
