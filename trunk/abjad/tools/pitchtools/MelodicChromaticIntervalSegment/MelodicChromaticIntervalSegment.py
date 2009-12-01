from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment
from abjad.tools.pitchtools.MelodicChromaticInterval import \
   MelodicChromaticInterval


class MelodicChromaticIntervalSegment(_IntervalSegment):
   '''.. versionadded:: 1.1.2

   '''

   def __init__(self, mci_tokens):
      for token in mci_tokens:
         mci = MelodicChromaticInterval(token)
         self.append(mci)

   ## OVERLOADS ##

   def __copy__(self):
      return MelodicChromaticIntervalSegment(self.intervals)

   ## PUBLIC ATTRIBUTES ##

   @property
   def harmonic_chromatic_interval_segment(self):
      from abjad.tools.pitchtools.HarmonicChromaticIntervalSegment import \
         HarmonicChromaticIntervalSegment
      return HarmonicChromaticIntervalSegment(self)
