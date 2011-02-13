from abjad.tools.pitchtools._IntervalClassSegment import _IntervalClassSegment
from abjad.tools.pitchtools.MelodicChromaticIntervalClass import MelodicChromaticIntervalClass


class MelodicChromaticIntervalClassSegment(_IntervalClassSegment):
   '''.. versionadded:: 1.1.2

   Abjad model of melodic chromatic interval-class segment::

      abjad> pitchtools.MelodicChromaticIntervalClassSegment([-2, -14, 3, 5.5, 6.5])
      MelodicChromaticIntervalClassSegment(-2, -2, +3, +5.5, +6.5)

   Melodic chromatic interval-class segments are immutable.
   '''

   def __new__(self, mcic_tokens):
      mcics = [ ]
      for mcic_token in mcic_tokens:
         mcic = MelodicChromaticIntervalClass(mcic_token)
         mcics.append(mcic)
      return tuple.__new__(self, mcics)
