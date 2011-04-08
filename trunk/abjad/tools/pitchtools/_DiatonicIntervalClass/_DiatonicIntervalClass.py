from abjad.tools.pitchtools._Diatonic import _Diatonic
from abjad.tools.pitchtools._IntervalClass import _IntervalClass


class _DiatonicIntervalClass(_IntervalClass, _Diatonic):
   '''.. versionadded:: 1.1.2

   Diatonic interval-class base class.
   '''

   ## OVERLOADS ##

   def __abs__(self):
      from abjad.tools.pitchtools.HarmonicDiatonicIntervalClass import HarmonicDiatonicIntervalClass
      return HarmonicDiatonicIntervalClass(str(self))

   def __float__(self):
      return float(self._number)

   def __int__(self):
      return self._number

   def __repr__(self):
      return "%s('%s')" % (self.__class__.__name__, str(self))

   ## PRIVATE ATTRIBUTES ##

   _acceptable_quality_strings = ('perfect', 'major', 'minor', 'diminished', 'augmented')

   _interval_number_to_interval_string = {1: 'unison', 2: 'second',
         3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth',
         7: 'seventh', 8: 'octave'}

   _quality_abbreviation_to_quality_string = {
      'M': 'major', 'm': 'minor', 'P': 'perfect', 'aug': 'augmented', 'dim': 'diminished'}

   _quality_string_to_quality_abbreviation = {
         'major': 'M', 'minor': 'm', 'perfect': 'P', 'augmented': 'aug', 'diminished': 'dim'}

   @property
   def _interval_string(self):
      return self._interval_number_to_interval_string[abs(self.number)]

   @property
   def _quality_abbreviation(self):
      return self._quality_string_to_quality_abbreviation[self._quality_string]
