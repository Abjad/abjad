from abjad.tools.pitchtools._PitchClassSegment import _PitchClassSegment
from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass
from abjad.tools.pitchtools.NumberedChromaticPitchClassSet import NumberedChromaticPitchClassSet
import copy


class NumberedChromaticPitchClassSegment(_PitchClassSegment):
   '''.. versionadded:: 1.1.2

   The Abjad model of a numbered chromatic pitch-class segment::

      abjad> pitchtools.NumberedChromaticPitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
      NumberedChromaticPitchClassSegment(10, 10.5, 6, 7, 10.5, 7)

   Numbered chromatic pitch-class segments are immutable.
   '''

   def __new__(self, pitch_class_tokens):
      pitch_classes = [NumberedChromaticPitchClass(x) for x in pitch_class_tokens]
      return tuple.__new__(self, pitch_classes)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s([%s])' % (self.__class__.__name__, self._repr_string)

   def __str__(self):
      return '<%s>' % self._format_string
      
   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   @property
   def _repr_string(self):
      return self._format_string

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class_segment(self):
      interval_classes = list(listtools.difference_series(self.pitch_classes))
      return InversionEquivalentChromaticIntervalClassSegment(interval_classes)

   @property
   def pitch_class_set(self):
      return NumberedChromaticPitchClassSet(self)

   @property
   def pitch_classes(self):
      return tuple(self[:])

   ## PUBLIC METHODS ##

   def invert(self):
      return NumberedChromaticPitchClassSegment([pc.invert( ) for pc in self])
      
   def multiply(self, n):
      return NumberedChromaticPitchClassSegment([pc.multiply(n) for pc in self])

   def retrograde(self):
      return NumberedChromaticPitchClassSegment(reversed(self))

   def rotate(self, n):
      from abjad.tools import listtools
      pitch_classes = listtools.rotate(self.pitch_classes, n)
      return NumberedChromaticPitchClassSegment(pitch_classes)
      
   def transpose(self, n):
      return NumberedChromaticPitchClassSegment([pc.transpose(n) for pc in self])
