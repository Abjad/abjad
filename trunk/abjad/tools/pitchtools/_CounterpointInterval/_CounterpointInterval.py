from abjad.tools.pitchtools._Interval import _Interval


class _CounterpointInterval(_Interval):

   ## PUBLIC ATTRIBUTES ##

   @property
   def number(self):
      return self._number

   @property
   def semitones(self):
      raise NotImplementedError
