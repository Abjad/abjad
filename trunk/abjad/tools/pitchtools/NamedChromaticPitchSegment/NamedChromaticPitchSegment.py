from abjad.tools import listtools
from abjad.tools.pitchtools._PitchSegment import _PitchSegment
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.HarmonicChromaticIntervalSegment import HarmonicChromaticIntervalSegment
from abjad.tools.pitchtools.MelodicChromaticIntervalSegment import MelodicChromaticIntervalSegment
from abjad.tools.pitchtools.HarmonicDiatonicIntervalSegment import HarmonicDiatonicIntervalSegment
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClassSegment import \
   InversionEquivalentChromaticIntervalClassSegment
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClassSet import \
   InversionEquivalentChromaticIntervalClassSet
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClassVector import \
   InversionEquivalentChromaticIntervalClassVector
from abjad.tools.pitchtools.MelodicDiatonicIntervalSegment import MelodicDiatonicIntervalSegment
from abjad.tools.pitchtools.NumberedChromaticPitchClassSet import NumberedChromaticPitchClassSet
from abjad.tools.pitchtools.NumberedChromaticPitchClassVector import NumberedChromaticPitchClassVector
from abjad.tools.pitchtools.NamedChromaticPitchSet import NamedChromaticPitchSet
from abjad.tools.pitchtools.NamedChromaticPitchVector import NamedChromaticPitchVector


class NamedChromaticPitchSegment(_PitchSegment):
   '''.. versionadded:: 1.1.2

   Ordered collection of pitch instances. ::

      abjad> pitch_segment = pitchtools.NamedChromaticPitchSegment([-2, -1.5, 6, 7, -1.5, 7])
      abjad> pitch_segment
      NamedChromaticPitchSegment(bf, bqf, fs', g', bqf, g')
   '''

   #def __init__(self, pitch_tokens):
   def __new__(self, pitch_tokens):
      pitches = [NamedChromaticPitch(x) for x in pitch_tokens]
      #self.extend(pitches)
      return tuple.__new__(self, pitches)

   ## OVERLOADS ##

   def __repr__(self):
      contents_string = ', '.join([str(x) for x in self])
      return '%s(%s)' % (self.__class__.__name__, contents_string)

   ## PUBLIC ATTRIBUTES ##

   @property
   def harmonic_chromatic_interval_class_segment(self):
      return [
         x.interval_class for x in self.harmonic_chromatic_interval_segment]

   @property
   def harmonic_chromatic_interval_segment(self):
      result = list(listtools.difference_series(self.numbers))
      result = [-x for x in result]
      return HarmonicChromaticIntervalSegment(result)

   @property
   def harmonic_diatonic_interval_class_segment(self):
      return [x.interval_class for x in self.harmonic_diatonic_interval_segment]

   @property
   def harmonic_diatonic_interval_segment(self):
      result = list(listtools.difference_series(self.pitches))
      result = [-x for x in result]
      return HarmonicDiatonicIntervalSegment(result)

   @property
   def inflection_point_count(self):
      return len(self.local_minima) + len(self.local_maxima)

   @property
   def interval_class_segment(self):
      pitch_classes = self.pitch_class_segment
      interval_classes = listtools.difference_series(pitch_classes)
      return InversionEquivalentChromaticIntervalClassSegment(interval_classes)

   @property
   def interval_class_set(self):
      pitch_classes = self.pitch_class_segment
      interval_classes = listtools.difference_series(pitch_classes)
      return InversionEquivalentChromaticIntervalClassSet(interval_classes)
      
   @property
   def interval_class_vector(self):
      pitch_classes = self.pitch_class_segment
      interval_classes = listtools.difference_series(pitch_classes)
      return InversionEquivalentChromaticIntervalClassVector(interval_classes)
      
   @property
   def local_minima(self):
      result = [ ]
      if 3 <= len(self):
         for i in range(1, len(self) - 1):
            left, middle, right = self[i-1], self[i], self[i+1]
            if middle < left and middle < right:
               result.append(middle)
      return tuple(result)

   @property
   def local_maxima(self):
      result = [ ]
      if 3 <= len(self):
         for i in range(1, len(self) - 1):
            left, middle, right = self[i-1], self[i], self[i+1]
            if left < middle and right < middle:
               result.append(middle)
      return tuple(result)

   @property
   def melodic_chromatic_interval_class_segment(self):
      return [x.interval_class for x in self.melodic_chromatic_interval_segment]

   @property
   def melodic_chromatic_interval_segment(self):
      result = list(listtools.difference_series(self.numbers))
      return MelodicChromaticIntervalSegment(result)

   @property
   def melodic_diatonic_interval_class_segment(self):
      return [x.interval_class for x in self.melodic_diatonic_interval_segment]

   @property
   def melodic_diatonic_interval_segment(self):
      result = list(listtools.difference_series(self.pitches))
      result = [-x for x in result]
      return MelodicDiatonicIntervalSegment(result)

   @property
   def numbers(self):
      return [pitch.pitch_number for pitch in self]

   @property
   def pitch_class_segment(self):
      from abjad.tools.pitchtools.NumberedChromaticPitchClassSegment import NumberedChromaticPitchClassSegment
      return NumberedChromaticPitchClassSegment([pitch.pitch_class for pitch in self])

   @property
   def pitch_class_set(self):
      return NumberedChromaticPitchClassSet([pitch.pitch_class for pitch in self])

   @property
   def pitch_class_vector(self):
      return PitchClassVector([pitch.pitch_class for pitch in self])

   @property
   def pitch_set(self):
      return NamedChromaticPitchSet(self[:])

   @property
   def pitch_vector(self):
      return PitchVector(self.pitches)

   @property
   def pitches(self):
      return self[:]

   ## PUBLIC METHODS ##

   def transpose(self, melodic_interval):
      '''Transpose pitches in pitch segment by melodic interval
      and emit new pitch segment.'''
      pitches = [pitch + melodic_interval for pitch in self]
      return NamedChromaticPitchSegment(pitches)
