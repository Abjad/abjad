from abjad.core import _Immutable
from abjad.core import _StrictComparator
from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.tools import durtools


class Meter(_StrictComparator, _Immutable):
   '''DEPRECATED.

   Use ``TimeSignatureMark`` instead.

   Abjad model of time signature::

      abjad> metertools.Meter((5, 32))
      Meter(5, 32)

   return meter.
   '''

   __slots__ = ('_denominator', '_duration', '_format', '_is_nonbinary',
      '_multiplier', '_numerator', '_partial', )

   def __init__(self, *args, **kwargs):

      ## initialize numerator and denominator from *args
      if len(args) == 1 and isinstance(args[0], Meter):
         meter = args[0]
         numerator, denominator = meter.numerator, meter.denominator
      elif len(args) == 1 and isinstance(args[0], durtools.Duration):
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
      if not isinstance(partial, (type(None), durtools.Duration)):
         raise TypeError
      object.__setattr__(self, '_partial', partial)

      ## initialize derived attributes
      object.__setattr__(self, '_duration', durtools.Duration(numerator, denominator))
      object.__setattr__(self, '_format', r'\time %s/%s' % (numerator, denominator))
      _multiplier = durtools.positive_integer_to_implied_prolation_multipler(self.denominator)
      object.__setattr__(self, '_multiplier', _multiplier)
      object.__setattr__(self, '_is_nonbinary', not mathtools.is_nonnegative_integer_power_of_two(self.denominator))

   ## OVERLOADS ##

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
      '''Duration duration of meter.'''
      return self._duration

   @property
   def format(self):
      '''LilyPond input format of meter.'''
      return self._format

   @property
   def multiplier(self):
      '''Duration prolation multiplier of meter.'''
      return self._multiplier

   @property
   def numerator(self):
      '''Integer numerator of meter.'''
      return self._numerator

   @property
   def is_nonbinary(self):
      '''Boolean indicator of nonbinary meter.'''
      return self._is_nonbinary

   @property
   def partial(self):
      '''Duration partial-measure pickup prior to meter.'''
      return self._partial
