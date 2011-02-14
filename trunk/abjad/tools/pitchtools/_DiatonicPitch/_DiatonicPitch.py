from abjad.tools.pitchtools._Pitch import _Pitch


class _DiatonicPitch(_Pitch):
   '''.. versionadded:: 1.1.2

   Base class for diatonic pitch classes.
   '''

   ## OVERLOADS ##

   def __abs__(self):
      return self._number

   def __float__(self):
      return float(self._number)

   def __int__(self):
      return self._number
