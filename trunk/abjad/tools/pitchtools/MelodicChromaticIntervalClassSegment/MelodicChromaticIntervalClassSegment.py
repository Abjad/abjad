from abjad.tools.pitchtools._IntervalClassSegment import _IntervalClassSegment
from abjad.tools.pitchtools.MelodicChromaticIntervalClass import MelodicChromaticIntervalClass


class MelodicChromaticIntervalClassSegment(_IntervalClassSegment):
   '''.. versionadded:: 1.1.2

   '''

   #def __init__(self, mcic_tokens):
   def __new__(self, mcic_tokens):
      mcics = [ ]
      for mcic_token in mcic_tokens:
         mcic = MelodicChromaticIntervalClass(mcic_token)
         #self.append(mcic)
         mcics.append(mcic)
      return tuple.__new__(self, mcics)
