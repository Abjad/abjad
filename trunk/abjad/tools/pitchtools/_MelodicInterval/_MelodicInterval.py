from abjad.tools.pitchtools._Interval import _Interval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval


class _MelodicInterval(_Interval):
   '''.. versionadded:: 1.1.2

   Directed melodic interval.
   '''

   ## OVERLOADS ##

   def __abs__(self):
      return _HarmonicInterval(self)

   def __eq__(self, arg):
      if isinstance(arg, self.__class__):
         if arg.interval_number == self.interval_number:
            if arg.direction_number == self.direction_number:
               return True
      return False

   def __ne__(self, arg):
      return not self == arg

   @staticmethod
   def __neg__(self):
      pass

   ## PUBLIC ATTRIBUTES ##

   @property
   def direction_number(self):
      return self._direction_number

   @property
   def direction_string(self):
      return self._direction_string
