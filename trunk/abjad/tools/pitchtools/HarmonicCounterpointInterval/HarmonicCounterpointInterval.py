from abjad.tools.pitchtools._CounterpointInterval import _CounterpointInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval
from abjad.tools.pitchtools.HarmonicCounterpointIntervalClass import HarmonicCounterpointIntervalClass


class HarmonicCounterpointInterval(_CounterpointInterval, _HarmonicInterval):
   '''.. versionadded:: 1.1.2

   Abjad model of harmonic counterpoint interval::

      abjad> pitchtools.HarmonicCounterpointInterval(-9)
      HarmonicCounterpointInterval(9)

   Harmonic counterpoint intervals are immutable.
   '''

   def __init__(self, token):
      from abjad.tools.pitchtools._DiatonicInterval import _DiatonicInterval
      if isinstance(token, int):
         _number = abs(token)
      elif isinstance(token, _DiatonicInterval):
         _number = abs(token.number)
      else:
         raise TypeError('must be number or diatonic interval.')
      object.__setattr__(self, '_number', _number)

   ## OVERLOADS ##
   
   def __eq__(self, arg):
      if isinstance(arg, HarmonicCounterpointInterval):
         if self.number == arg.number:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class(self):
      return HarmonicCounterpointIntervalClass(self)
