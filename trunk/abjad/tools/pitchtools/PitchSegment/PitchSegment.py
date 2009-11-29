from abjad.pitch import Pitch
from abjad.tools import listtools
from abjad.tools.pitchtools.HarmonicChromaticInterval import \
   HarmonicChromaticInterval
from abjad.tools.pitchtools.MelodicChromaticInterval import \
   MelodicChromaticInterval


class PitchSegment(list):
   '''.. versionadded:: 1.1.2

   Ordered collection of pitch instances. ::

      abjad> pitch_segment = pitchtools.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
      abjad> pitch_segment
      PitchSegment(bf, bqf, fs', g', bqf, g')
   '''

   def __init__(self, pitch_tokens):
      pitches = [Pitch(x) for x in pitch_tokens]
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
      result = list(listtools.difference_series(self.pitch_numbers))
      return [HarmonicChromaticInterval(n) for n in result]

   @property
   def harmonic_diatonic_interval_class_segment(self):
      return [x.interval_class for x in self.harmonic_diatonic_interval_segment]

   @property
   def harmonic_diatonic_interval_segment(self):
      return [abs(x) for x in self.melodic_diatonic_interval_segment]

   @property
   def inflection_point_count(self):
      return len(self.local_minima) + len(self.local_maxima)

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
      result = list(listtools.difference_series(self.pitch_numbers))
      return [MelodicChromaticInterval(n) for n in result]

   @property
   def melodic_diatonic_interval_class_segment(self):
      return [x.interval_class for x in self.melodic_diatonic_interval_segment]

   @property
   def melodic_diatonic_interval_segment(self):
      melodic_diatonic_intervals = [ ]
      for left_pitch, right_pitch in listtools.pairwise(self):
         melodic_diatonic_interval = left_pitch - right_pitch
         melodic_diatonic_intervals.append(melodic_diatonic_interval)
      return melodic_diatonic_intervals

   @property
   def pitch_numbers(self):
      return [pitch.number for pitch in self]
