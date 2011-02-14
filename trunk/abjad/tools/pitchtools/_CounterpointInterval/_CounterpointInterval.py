from abjad.tools.pitchtools._Interval import _Interval


## TODO: implement _CounterpointObject
class _CounterpointInterval(_Interval):

   ## OVERLOADS ##

   def __abs__(self):
      return type(self)(abs(self._number))

   def __float__(self):
      return float(self._number)

   def __int__(self):
      return self._number

   ## PUBLIC ATTRIBUTES ##

   @property
   def number(self):
      return self._number

   @property
   def semitones(self):
      raise NotImplementedError
