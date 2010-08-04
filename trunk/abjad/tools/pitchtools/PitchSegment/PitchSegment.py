from abjad.NamedPitch import NamedPitch
from abjad.tools import listtools
from abjad.tools.pitchtools.HarmonicChromaticIntervalSegment import \
   HarmonicChromaticIntervalSegment
from abjad.tools.pitchtools.MelodicChromaticIntervalSegment import \
   MelodicChromaticIntervalSegment
from abjad.tools.pitchtools.HarmonicDiatonicIntervalSegment import \
   HarmonicDiatonicIntervalSegment
from abjad.tools.pitchtools.IntervalClassSegment import \
   IntervalClassSegment
from abjad.tools.pitchtools.IntervalClassSet import \
   IntervalClassSet
from abjad.tools.pitchtools.IntervalClassVector import \
   IntervalClassVector
from abjad.tools.pitchtools.MelodicDiatonicIntervalSegment import \
   MelodicDiatonicIntervalSegment
from abjad.tools.pitchtools.PitchClassSet import PitchClassSet
from abjad.tools.pitchtools.PitchClassVector import PitchClassVector
from abjad.tools.pitchtools.PitchSet import PitchSet
from abjad.tools.pitchtools.PitchVector import PitchVector


class PitchSegment(list):
   '''.. versionadded:: 1.1.2

   Ordered collection of pitch instances. ::

      abjad> pitch_segment = pitchtools.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
      abjad> pitch_segment
      PitchSegment(bf, bqf, fs', g', bqf, g')
   '''

   def __init__(self, pitch_tokens):
      pitches = [NamedPitch(x) for x in pitch_tokens]
      self.extend(pitches)

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
      return IntervalClassSegment(interval_classes)

   @property
   def interval_class_set(self):
      pitch_classes = self.pitch_class_segment
      interval_classes = listtools.difference_series(pitch_classes)
      return IntervalClassSet(interval_classes)
      
   @property
   def interval_class_vector(self):
      pitch_classes = self.pitch_class_segment
      interval_classes = listtools.difference_series(pitch_classes)
      return IntervalClassVector(interval_classes)
      
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
      return [pitch.number for pitch in self]

   @property
   def pitch_class_segment(self):
      from abjad.tools.pitchtools.PitchClassSegment import PitchClassSegment
      return PitchClassSegment([pitch.pitch_class for pitch in self])

   @property
   def pitch_class_set(self):
      return PitchClassSet([pitch.pitch_class for pitch in self])

   @property
   def pitch_class_vector(self):
      return PitchClassVector([pitch.pitch_class for pitch in self])

   @property
   def pitch_set(self):
      return PitchSet(self[:])

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
      return PitchSegment(pitches)
