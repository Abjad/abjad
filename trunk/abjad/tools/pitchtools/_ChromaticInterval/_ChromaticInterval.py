from abjad.tools import mathtools
from abjad.tools.pitchtools._Interval import _Interval


class _ChromaticInterval(_Interval):
   '''.. versionaddedd:: 1.1.2

   Abstract chromatic interval class from which concrete classes inherit.
   '''

   def __init__(self, arg):
      if isinstance(arg, (int, float, long)):
         #self._number = arg
         _number = arg
      elif isinstance(arg, _Interval):
         #self._number = arg.semitones
         _number = arg.semitones
      else:
         raise TypeError('%s must be number or interval.' % arg)
      object.__setattr__(self, '_number', _number)

   ## OVERLOADS ##

   def __abs__(self):
      from abjad.tools.pitchtools.HarmonicChromaticInterval import HarmonicChromaticInterval
      return HarmonicChromaticInterval(abs(self._number))

   def __add__(self, arg):
      if isinstance(arg, self.__class__):
         number = self.number + arg.number
         return self.__class__(number)
      raise TypeError('must be %s.'% self.__class__)

   def __copy__(self):
      return self.__class__(self.number)

   def __eq__(self, arg):
      if isinstance(arg, self.__class__):
         if self.number == arg.number:
            return True
      return False

   def __float__(self):
      return float(self._number)

   def __int__(self):
      return int(self._number)

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._number)

   def __str__(self):
      return '%s' % self.number

   def __sub__(self, arg):
      if isinstance(arg, self.__class__):
         number = self.number - arg.number
         return self.__class__(number)
      raise TypeError('must be %s' % self.__class__)

   ## PUBLIC ATTRIBUTES ##

   @property
   def number(self):
      return self._number

   @property
   def semitones(self):
      return self.number
