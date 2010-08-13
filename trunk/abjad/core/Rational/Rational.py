class Rational(object):
   '''Abjad rational number class.'''

   def __init__(self, *args):
      if not args:
         numerator, denominator = 0, 1
      elif len(args) == 1 and isinstance(args[0], (int, long)):
         numerator, denominator = args[0], 1
      elif len(args) == 1 and isinstance(args[0], Rational):
         rational = args[0]
         numerator, denominator = rational.numerator, rational.denominator
      elif len(args) == 2:
         n, d = args
         if not isinstance(n, (int, long)):
            raise TypeError('must be int or long.')
         if not isinstance(d, (int, long)):
            raise TypeError('must be int or long.')
         if d == 0:
            raise ZeroDivisionError
         gcd = self._gcd(n, d)
         numerator = n / gcd
         denominator = d / gcd
      else:
         raise TypeError
      super(Rational, self).__setattr__('_numerator', numerator)
      super(Rational, self).__setattr__('_denominator', denominator)

   ## OVERLOADS ##

   def __abs__(self):
      return Rational(abs(self.numerator), self.denominator)

   def __add__(self, arg):
      if isinstance(arg, Rational):
         return Rational(
            self.numerator * arg.denominator + self.denominator * 
            arg.numerator, self.denominator * arg.denominator)
      elif isinstance(arg, (int, long)):
         return Rational(self.numerator + arg * self.denominator, self.denominator)
      elif isinstance(arg, float):
         return float(self) + arg
      else:
         raise ValueError

   def __delattr__(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)

   def __div__(self, arg):
      if arg == 0:
         raise(ZeroDivisionError)
      if isinstance(arg, Rational):
         return Rational(self.numerator * arg.denominator, self.denominator * arg.numerator)
      elif isinstance(arg, (int, long)):
         return Rational(self.numerator, self.denominator * arg)
      elif isinstance(arg, float):
         return float(self) / arg

   def __eq__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self.numerator == self.denominator * arg
      else:
         return False

   def __float__(self):
      return float(self.numerator) / float(self.denominator)

   def __floordiv__(self, arg):
      from math import floor
      return Rational(int(floor(float(self / arg))))

   def __ge__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self.numerator >= self.denominator * arg
      else:
         raise TypeError

   def __gt__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self.numerator > self.denominator * arg
      else:
         raise TypeError

   def __int__(self):
      result = abs(self.numerator) // abs(self.denominator)
      if 0 <= self:
         return result
      else:
         return -result

   ## COMPATIBILITY: removed because the Python 2.6 Fraction
   ##                class does not implement __invert__( ).
   #def __invert__(self):
   #   return Rational(self.denominator, self.numerator)

   def __le__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self.numerator <= self.denominator * arg
      else:
         raise TypeError

   def __long__(self):
      return long(int(self))

   def __lt__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return self.numerator < self.denominator * arg
      else:
         raise TypeError

   def __mul__(self, arg):
      if isinstance(arg, Rational):
         return Rational(self.numerator * arg.numerator, self.denominator * arg.denominator)
      elif isinstance(arg, (int, long)):
         return Rational(self.numerator * arg, self.denominator)
      elif isinstance(arg, float):
         return float(self) * arg
      else:
         raise ValueError

   def __mod__(self, arg):
      return self - self // arg * arg

   def __ne__(self, arg):
      if isinstance(arg, (int, float, long, Rational)):
         return not self == arg
      else:
         return True

   def __neg__(self):
      return Rational(-self.numerator, self.denominator)

   def __pow__(self, arg):
      assert isinstance(arg, int)
      if 0 < arg:
         result = Rational(self.numerator, self.denominator)
         for i in range(arg - 1):
            result *= self
      elif arg == 0:
         return Rational(1)
      elif arg < 0:
         #result = ~self
         result = Rational(self.denominator, self.numerator)
         for i in range(abs(arg) - 1):
            #result *= ~self
            result *= Rational(self.denominator, self.numerator)
      return result

   def __radd__(self, arg):
      return self + arg
      
   def __rdiv__(self, arg):
      if arg == 0:
         return arg
      #return ~(self / arg)
      tmp = self / arg
      return Rational(tmp.denominator, tmp.numerator)

   def __repr__(self):
      return '%s(%s, %s)' % (self.__class__.__name__, self.numerator, self.denominator)

   def __rfloordiv__(self, arg):
      from math import floor
      return Rational(int(floor(float(arg / self))))

   def __rmul__(self, arg):
      return self * arg
   
   def __rmod__(self, arg):
      return arg - arg // self * self

   def __rsub__(self, arg):
      return arg + -self

   def __rtruediv__(self, arg):
      return arg / self

   def __setattr__(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)

   def __str__(self):
      if self.denominator == 1:
         return '%s' % self.numerator
      else:
         return '%s/%s' % (self.numerator, self.denominator)

   def __sub__(self, arg):
      return self + -arg

   def __truediv__(self, arg):
      return self / arg

#   ## PRIVATE ATTRIBUTES ##
#
#   @property
#   def _d(self):
#      return self.denominator
#
#   @property
#   def _n(self):
#      return self.numerator

   ## PRIVATE METHODS ##

   def _gcd(self, a, b):
       if b == 0: 
         return a
       return self._gcd(b, a % b)

   ## PUBLIC ATTRIBUTES ##

   @property
   def denominator(self):
      return self._denominator

   @property
   def numerator(self):
      return self._numerator
