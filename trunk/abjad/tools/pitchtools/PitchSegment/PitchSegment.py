from abjad.pitch import Pitch
from abjad.tools import listtools
from abjad.tools.pitchtools.ChromaticInterval import ChromaticInterval


class PitchSegment(list):
   '''.. versionadded:: 1.1.2

   Ordered collection of pitches.
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
      chromatic_interval_segment = [ ]
      for left, right in listtools.pairwise(self):
         chromatic_interval_number = right.number - left.number
         chromatic_interval = ChromaticInterval(chromatic_interval_number)
         chromatic_interval_segment.append(chromatic_interval)
      return chromatic_interval_segment

   @property
   def chromatic_interval_class_segment(self):
      result = self.chromatic_interval_segment
      result = [x.interval_class for x in result]
      return result
