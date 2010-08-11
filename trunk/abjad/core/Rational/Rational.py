class Rational(object):
   '''Abjad rational number class.'''

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], (int, long)):
         #self._numerator = args[0]
         #self._denominator = 1
         numerator, denominator = args[0], 1
      elif len(args) == 1 and isinstance(args[0], Rational):
         rational = args[0]
         #self._numerator = rational._numerator
         #self._denominator = rational._denominator
         numerator, denominator = rational._numerator, rational._denominator
      elif len(args) == 1 and isinstance(args[0], tuple):
         #self.__init__(*args[0])
         numerator, denominator = args[0]
      elif len(args) == 2:
         n, d = args
         if not isinstance(n, (int, long)):
            raise TypeError('must be int or long.')
         if not isinstance(d, (int, long)):
            raise TypeError('must be int or long.')
         if d == 0:
            raise ZeroDivisionError
         gcd = self._gcd(n, d)
         #self._numerator = n / gcd
         #self._denominator = d / gcd
         numerator = n / gcd
         denominator = d / gcd
      else:
         raise TypeError
      super(Rational, self).__setattr__('_numerator', numerator)
      super(Rational, self).__setattr__('_denominator', denominator)

   ## PRIVATE METHODS ##

   def _gcd(self, a, b):
       if b == 0: 
         return a
       return self._gcd(b, a % b)

   ## OVERLOADS ##

   def __delattr__(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)

   def __repr__(self):
      return '%s(%s, %s)' % (self.__class__.__name__, self._n, self._d)

   def __setattr__(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)

   def __str__(self):
      if self._d == 1:
         return '%s' % self._n
      else:
         return '%s/%s' % (self._n, self._d)

   ## PROPERTIES ##

   @property
   def _n(self):
      return self._numerator

   @property
   def _d(self):
      return self._denominator

   ## ARITHMETIC OPERATORS ##

   def __neg__(self):
      return Rational(-self._n, self._d)

   def __invert__(self):
      return Rational(self._d, self._n)

   def __abs__(self):
      return Rational(abs(self._n), self._d)

   def __eq__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self._n == self._d * arg
      else:
         return False

   def __ne__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return not self == arg
      else:
         return True

   def __ge__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self._n >= self._d * arg
      else:
         raise TypeError

   def __gt__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self._n > self._d * arg
      else:
         raise TypeError

   def __le__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self._n <= self._d * arg
      else:
         raise TypeError

   def __lt__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self._n < self._d * arg
      else:
         raise TypeError

   def  __add__(self, arg):
      if isinstance(arg, Rational):
         return Rational(
            self._n * arg._d + self._d * arg._n, self._d * arg._d)
      elif isinstance(arg, (int, long)):
         return Rational(self._n + arg * self._d, self._d)
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
         return Rational(self._n * arg._n, self._d * arg._d)
      elif isinstance(arg, (int, long)):
         return Rational(self._n * arg, self._d)
      elif isinstance(arg, float):
         return float(self) * arg
      else:
         raise ValueError

   def __rmul__(self, arg):
      return self * arg
   
   def __div__(self, arg):
      if arg == 0:
         raise(ZeroDivisionError)
      if isinstance(arg, Rational):
         return Rational(self._n * arg._d, self._d * arg._n)
      elif isinstance(arg, (int, long)):
         return Rational(self._n, self._d * arg)
      elif isinstance(arg, float):
         return float(self) / arg

   def __rdiv__(self, arg):
      if arg == 0:
         return arg
      return ~(self / arg)

   def __truediv__(self, arg):
      return self / arg

   def __rtruediv__(self, arg):
      return arg / self

   def __floordiv__(self, arg):
      from math import floor
      return Rational(int(floor(float(self / arg))))

   def __rfloordiv__(self, arg):
      from math import floor
      return Rational(int(floor(float(arg / self))))

   def __pow__(self, arg):
      assert isinstance(arg, int)
      if arg > 0:
         result = Rational(self._n, self._d)
         for i in range(arg - 1):
            result *= self
      elif arg == 0:
         return Rational(1)
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
