from abjad.pitch import Pitch
from abjad.tools import listtools
from abjad.tools.pitchtools.ChromaticInterval import ChromaticInterval


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
   def chromatic_interval_segment(self):
      result = list(listtools.difference_series(self.chromatic_pitch_numbers))
      return [ChromaticInterval(n) for n in result]

   @property
   def chromatic_interval_class_segment(self):
      return [x.interval_class for x in self.chromatic_interval_segment]

   @property
   def chromatic_pitch_numbers(self):
      return [pitch.number for pitch in self]

   @property
   def diatonic_interval_segment(self):
      return list(listtools.difference_series(self))

   @property
   def diatonic_interval_class_segment(self):
      return [x.interval_class for x in self.diatonic_interval_segment]

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
