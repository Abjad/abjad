from abjad.tools.pitchtools._IntervalClassSegment import _IntervalClassSegment
from abjad.tools.pitchtools.MelodicChromaticIntervalClass import MelodicChromaticIntervalClass


class MelodicChromaticIntervalClassSegment(_IntervalClassSegment):
   '''.. versionadded:: 1.1.2

   '''

   def __init__(self, mcic_tokens):
      for mcic_token in mcic_tokens:
         mcic = MelodicChromaticIntervalClass(mcic_token)
         self.append(mcic)
