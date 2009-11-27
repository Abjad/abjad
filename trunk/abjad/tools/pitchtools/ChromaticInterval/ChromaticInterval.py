from abjad.tools import mathtools
from abjad.tools.pitchtools.DiatonicInterval import DiatonicInterval


class ChromaticInterval(object):
   '''.. versionaddedd:: 1.1.2

   Chromatic interval in semitones. ::

      abjad> pitchtools.ChromaticInterval(-2)
      ChromaticInterval(-2)
   '''

   def __init__(self, arg):
      if isinstance(arg, (int, float, long)):
         self._interval_number = arg
      elif isinstance(arg, ChromaticInterval):
         self._interval_number = arg.interval
      elif isinstance(arg, DiatonicInterval):
         self._interval_number = arg.semitones
      else:
         raise TypeError

   ## OVERLOADS ##

   def __abs__(self):
      return ChromaticInterval(abs(self._interval_number))

   def __add__(self, arg):
      if isinstance(arg, ChromaticInterval):
         return ChromaticInterval(self._interval_number + arg._interval_number)
      else:
         raise TypeError

   def __copy__(self):
      return ChromaticInterval(self)

   def __eq__(self, arg):
      if isinstance(arg, ChromaticInterval):
         return self._interval_number == arg._interval_number
      else:
         raise TypeError

   def __float__(self):
      return float(self._interval_number)

   def __int__(self):
      return int(self._interval_number)

   def __ne__(self, arg):
      return not self == arg

   def __neg__(self):
      return ChromaticInterval(-self._interval_number)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._interval_number)

   def __sub__(self, arg):
      if isinstance(arg, ChromaticInterval):
         return ChromaticInterval(self._interval_number - arg._interval_number)
      else:
         raise TypeError

   ## PUBLIC ATTRIBUTES ##

   @property
   def direction_number(self):
      return mathtools.sign(self.interval_number) 

   @property
   def interval_class(self):
      return self.direction_number * (abs(self.interval_number) % 12)

   @property
   def interval_number(self):
      return self._interval_number

   @property
   def semitones(self):
      return self.interval_number
