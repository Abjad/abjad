from abjad.tools.pitchtools.PitchClass import PitchClass


class PitchClassSegment(list):
   '''.. versionadded:: 1.1.2

   Ordered collection of pitch class instances. ::
   '''

   def __init__(self, pitch_class_tokens):
      pitch_classes = [PitchClass(x) for x in pitch_class_tokens]
      self.extend(pitch_classes)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class_segment(self):
      interval_classes = list(listtools.difference_series(self.pitch_classes))
      return IntervalClassSegment(interval_classes)
