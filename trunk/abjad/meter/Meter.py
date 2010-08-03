from abjad.core.grobhandler import _GrobHandler
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import mathtools
import types


class Meter(_GrobHandler):

   def __init__(self, *args):
      _GrobHandler.__init__(self, 'TimeSignature')
      if len(args) == 1 and isinstance(args[0], Meter):
         meter = args[0]
         self.numerator = meter.numerator
         self.denominator = meter.denominator
      elif len(args) == 1 and isinstance(args[0], Rational):
         self.numerator = args[0]._n
         self.denominator = args[0]._d
      elif len(args) == 1 and isinstance(args[0], tuple):
         numerator, denominator = args[0][0], args[0][1]
         self.numerator = numerator
         self.denominator = denominator
      elif len(args) == 2 and all([isinstance(x, int) for x in args]):
         self.numerator = args[0]
         self.denominator = args[1]
      else:
         raise TypeError('invalid %s meter initialization.' % str(args))
      self._partial = None

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, Meter):
         return self.numerator == arg.numerator and \
            self.denominator == arg.denominator
      elif isinstance(arg, tuple):
         return self.numerator == arg[0] and self.denominator == arg[1]
      else:
         return False

   def __ge__(self, arg):
      if isinstance(arg, Meter):
         return self.duration >= arg.duration
      else:
         raise TypeError
   
   def __gt__(self, arg):
      if isinstance(arg, Meter):
         return self.duration > arg.duration
      else:
         raise TypeError
   
   def __le__(self, arg):
      if isinstance(arg, Meter):
         return self.duration <= arg.duration
      else:
         raise TypeError
   
   def __lt__(self, arg):
      if isinstance(arg, Meter):
         return self.duration < arg.duration
      else:
         raise TypeError
   
   def __ne__(self, arg):
      return not self == arg

   def __nonzero__(self):
      return True
   
   def __repr__(self):
      return 'Meter(%s, %s)' % (self.numerator, self.denominator)

   def __str__(self):
      return '%s/%s' % (self.numerator, self.denominator)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def denominator( ):
      def fget(self):
         return self._denominator
      def fset(self, arg):
         assert isinstance(arg, int)
         self._denominator = arg
      return property(**locals( ))

   @property
   def duration(self):
      return Rational(self.numerator, self.denominator)

   @property
   def format(self):
      return r'\time %s/%s' % (self.numerator, self.denominator)

   @property
   def multiplier(self):
      return durtools.positive_integer_to_implied_prolation_multipler(self.denominator)

   @property
   def nonbinary(self):
      return not mathtools.is_power_of_two(self.denominator)

   @apply
   def numerator( ):
      def fget(self):
         return self._numerator
      def fset(self, arg):
         assert isinstance(arg, int)
         self._numerator = arg
      return property(**locals( ))

   @apply
   def partial( ):
      r'''Rational-valued duration of pick-up at beginning of score.'''
      def fget(self):
         return self._partial
      def fset(self, arg):
         if not isinstance(arg, (Rational, types.NoneType)):
            raise TypeError('%s must be rational.' % arg)
         self._partial = arg
      return property(**locals( ))
