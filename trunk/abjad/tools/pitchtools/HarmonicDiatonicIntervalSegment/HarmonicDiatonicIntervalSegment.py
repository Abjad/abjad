from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment
from abjad.tools.pitchtools.HarmonicDiatonicInterval import HarmonicDiatonicInterval


class HarmonicDiatonicIntervalSegment(_IntervalSegment):
   '''.. versionadded:: 1.1.2

   Ordered collection of harmonic diatonic intervals.
   '''

   #def __init__(self, harmonic_diatonic_interval_tokens):
   def __new__(self, harmonic_diatonic_interval_tokens):
      hdis = [ ]
      for token in harmonic_diatonic_interval_tokens:
         hdi = HarmonicDiatonicInterval(token)
         #self.append(hdi)
         hdis.append(hdi)
      return tuple.__new__(self, hdis)

   ## OVERLOADS ##

   def __copy__(self):
      return HarmonicDiatonicIntervalSegment(self.intervals)

   ## PUBLIC ATTRIBUTES ##

   @property
   def harmonic_chromatic_interval_segment(self):
      from abjad.tools.pitchtools.HarmonicChromaticIntervalSegment import HarmonicChromaticIntervalSegment
      return HarmonicChromaticIntervalSegment(self)

   @property
   def melodic_chromatic_interval_segment(self):
      from abjad.tools.pitchtools.MelodicChromaticIntervalSegment import MelodicChromaticIntervalSegment
      return MelodicChromaticIntervalSegment(self)

   @property
   def melodic_diatonic_interval_segment(self):
      from abjad.tools.pitchtools.MelodicDiatonicIntervalSegment import MelodicDiatonicIntervalSegment
      return MelodicDiatonicIntervalSegment(self)
