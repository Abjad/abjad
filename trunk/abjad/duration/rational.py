# class: Rational.
#
# primary authors: Trevor Baca, Victor Adan.
# optimization: Jared Grubb.
# mailto: trevorbaca (at) gmail (dot) com.
# revision: 6

class Rational(object):

   def __init__(self, n, d = 1):
      assert isinstance(n, (int, long))
      assert isinstance(d, (int, long))
      assert d != 0
      gcd = self._gcd(n, d)
      self._n = n / gcd
      self._d = d / gcd

   ### INIT UTILS ###

   def _gcd(self, a, b):
       if b == 0: 
         return a
       return self._gcd(b, a % b)

   ### REPR ###

   def __repr__(self):
      return 'Rational(%s, %s)' % self.pair

   def __str__(self):
      if self._d == 1:
         return '%s' % self._n
      else:
         return '%s/%s' % (self._n, self._d)

   ### PROPERTIES ###

   @property
   def numerator(self):
      return self._n

   @property
   def denominator(self):
      return self._d

   @property
   def pair(self):
      return self._n, self._d

   ### ARITHMETIC OPERATORS ###

   def __neg__(self):
      return self.__class__(-self._n, self._d)

   def __invert__(self):
      return self.__class__(self._d, self._n)

   def __abs__(self):
      return self.__class__(abs(self._n), self._d)

   def __eq__(self, arg):
      return self._n == self._d * arg

   def __ne__(self, arg):
      return not self == arg

   def __gt__(self, arg):
       return self._n > self._d * arg

   def __ge__(self, arg):
       return self._n >= self._d * arg

   def __lt__(self, arg):
       return self._n < self._d * arg

   def __le__(self, arg):
       return self._n <= self._d * arg

   def  __add__(self, arg):
      if isinstance(arg, Rational):
         return self.__class__(
            self._n * arg._d + self._d * arg._n, self._d * arg._d)
      elif isinstance(arg, (int, long)):
         return self.__class__(self._n + arg * self._d, self._d)
      elif isinstance(arg, float):
         return float(self) + arg
      else:
         raise ValueError

   def __radd__(self, arg):
      return self + arg
      
   def __sub__(self, arg):
      return self + -arg

   def __rsub__(self, arg):
      return arg + -self

   def __mul__(self, arg):
      if isinstance(arg, Rational):
         return self.__class__(self._n * arg._n, self._d * arg._d)
      elif isinstance(arg, (int, long)):
         return self.__class__(self._n * arg, self._d)
      elif isinstance(arg, float):
         return float(self) * arg
      else:
         raise ValueError

   def __rmul__(self, arg):
      return self * arg
   
   def __div__(self, arg):
      if isinstance(arg, Rational):
         return self.__class__(self._n * arg._d, self._d * arg._n)
      elif isinstance(arg, (int, long)):
         return self.__class__(self._n, self._d * arg)
      elif isinstance(arg, float):
         return float(self) / arg

   def __rdiv__(self, arg):
      return ~(self / arg)

   def __truediv__(self, arg):
      return self / arg

   def __rtruediv__(self, arg):
      return arg / self

   def __floordiv__(self, arg):
      from math import floor
      return self.__class__(int(floor(float(self / arg))))

   def __rfloordiv__(self, arg):
      from math import floor
      return self.__class__(int(floor(float(arg / self))))

   def __pow__(self, arg):
      assert isinstance(arg, int)
      if arg > 0:
         result = self.copy( )
         for i in range(arg - 1):
            result *= self
      elif arg == 0:
         return self.__class__(1)
      elif arg < 0:
         result = ~self
         for i in range(abs(arg) - 1):
            result *= ~self
      return result

   def __mod__(self, arg):
      return self - self // arg * arg

   def __rmod__(self, arg):
      return arg - arg // self * self

   def __int__(self):
      result = abs(self._n) // abs(self._d)
      if self >= 0:
         return result
      else:
         return -result

   def __long__(self):
      return long(int(self))

   def __float__(self):
      return float(self._n) / float(self._d)
