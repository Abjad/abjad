from abjad.core import _Abjad
from abjad.core import _Immutable
from abjad.core import Rational
from abjad.tools import durtools
from abjad.tools import mathtools


class Meter(_Abjad, _Immutable):

   __slots__ = ('_denominator', '_duration', '_format', '_multiplier',
      '_nonbinary', '_numerator', '_partial', )

   def __init__(self, *args, **kwargs):

      ## initialize numerator and denominator from *args
      if len(args) == 1 and isinstance(args[0], Meter):
         meter = args[0]
         numerator, denominator = meter.numerator, meter.denominator
      elif len(args) == 1 and isinstance(args[0], Rational):
         numerator, denominator = args[0].numerator, args[0].denominator
      elif len(args) == 1 and isinstance(args[0], tuple):
         numerator, denominator = args[0][0], args[0][1]
      elif len(args) == 2 and all([isinstance(x, int) for x in args]):
         numerator, denominator = args[0], args[1]
      else:
         raise TypeError('invalid %s meter initialization.' % str(args))
      object.__setattr__(self, '_numerator', numerator)
      object.__setattr__(self, '_denominator', denominator)

      ## initialize partial from **kwargs
      partial = kwargs.get('partial', None)
      if not isinstance(partial, (type(None), Rational)):
         raise TypeError
      object.__setattr__(self, '_partial', partial)

      ## initialize derived attributes
      object.__setattr__(self, '_duration', Rational(numerator, denominator))
      object.__setattr__(self, '_format', r'\time %s/%s' % (numerator, denominator))
      _multiplier = durtools.positive_integer_to_implied_prolation_multipler(self.denominator)
      object.__setattr__(self, '_multiplier', _multiplier)
      object.__setattr__(self, '_nonbinary', not mathtools.is_power_of_two(self.denominator))

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(self)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, Meter):
         return self.numerator == arg.numerator and self.denominator == arg.denominator
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
      return '%s(%s, %s)' % (self.__class__.__name__, self.numerator, self.denominator)

   def __str__(self):
      return '%s/%s' % (self.numerator, self.denominator)

   ## PUBLIC ATTRIBUTES ##

   @property
   def denominator(self):
      '''Integer denominator of meter.'''
      return self._denominator

   @property
   def duration(self):
      '''Rational duration of meter.'''
      return self._duration

   @property
   def format(self):
      '''LilyPond input format of meter.'''
      return self._format

   @property
   def multiplier(self):
      '''Rational prolation multiplier of meter.'''
      return self._multiplier

   @property
   def numerator(self):
      '''Integer numerator of meter.'''
      return self._numerator

   @property
   def nonbinary(self):
      '''Boolean indicator of nonbinary meter.'''
      return self._nonbinary

   @property
   def partial(self):
      '''Rational partial-measure pickup prior to meter.'''
      return self._partial
