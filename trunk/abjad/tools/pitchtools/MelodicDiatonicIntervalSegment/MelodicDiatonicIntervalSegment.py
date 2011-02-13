from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment
from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval


class MelodicDiatonicIntervalSegment(_IntervalSegment):
   '''.. versionadded:: 1.1.2

   Abjad model of melodic diatonic interval segment::

      abjad> pitchtools.MelodicDiatonicIntervalSegment('M2 M9 -m3 -P4')
      MelodicDiatonicIntervalSegment('+M2 +M9 -m3 -P4')

   Melodic diatonic interval segments are immutable.
   '''

   def __new__(self, arg):
      if isinstance(arg, str):
         melodic_diatonic_interval_tokens = arg.split( )
      else:
         melodic_diatonic_interval_tokens = arg
      mdis = [ ]
      for token in melodic_diatonic_interval_tokens:
         mdi = MelodicDiatonicInterval(token)
         mdis.append(mdi)
      return tuple.__new__(self, mdis)

   ## OVERLOADS ##

   def __copy__(self):
      return MelodicDiatonicIntervalSegment(self.intervals)

   def __repr__(self):
      return "%s('%s')" % (self.__class__.__name__, ' '.join([str(x) for x in self]))

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
