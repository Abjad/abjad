from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment
from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval


class MelodicDiatonicIntervalSegment(_IntervalSegment):
   '''.. versionadded:: 1.1.2

   Ordered collection of melodic diatonic intervals.
   '''

   def __init__(self, melodic_diatonic_interval_tokens):
      for token in melodic_diatonic_interval_tokens:
         mdi = MelodicDiatonicInterval(token)
         self.append(mdi)

   ## OVERLOADS ##

   def __copy__(self):
      return MelodicDiatonicIntervalSegment(self.intervals)

   ## PUBLIC ATTRIBUTES ##

   @property
   def harmonic_chromatic_interval_segment(self):
      from abjad.tools.pitchtools.HarmonicChromaticIntervalSegment import HarmonicChromaticIntervalSegment
      return HarmonicChromaticIntervalSegment(self.intervals)

   @property
   def harmonic_diatonic_interval_segment(self):
      from abjad.tools.pitchtools.HarmonicDiatonicIntervalSegment import HarmonicDiatonicIntervalSegment
      return HarmonicDiatonicIntervalSegment(self.intervals)

   @property
   def melodic_chromatic_interval_segment(self):
      from abjad.tools.pitchtools.MelodicChromaticIntervalSegment import MelodicChromaticIntervalSegment
      return MelodicChromaticIntervalSegment(self.intervals)
