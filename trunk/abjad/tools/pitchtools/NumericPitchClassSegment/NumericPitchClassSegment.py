from abjad.tools.pitchtools.NumericPitchClass import NumericPitchClass
from abjad.tools.pitchtools.NumericPitchClassSet import NumericPitchClassSet
import copy


class NumericPitchClassSegment(list):
   '''.. versionadded:: 1.1.2

   Ordered collection of pitch class instances.
   '''

   def __init__(self, pitch_class_tokens):
      pitch_classes = [NumericPitchClass(x) for x in pitch_class_tokens]
      self.extend(pitch_classes)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '<%s>' % self._format_string
      
   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class_segment(self):
      interval_classes = list(listtools.difference_series(self.pitch_classes))
      return InversionEquivalentChromaticIntervalClassSegment(interval_classes)

   @property
   def pitch_class_set(self):
      return NumericPitchClassSet(self)

   @property
   def pitch_classes(self):
      return tuple(self[:])

   ## PUBLIC METHODS ##

   def invert(self):
      return NumericPitchClassSegment([pc.invert( ) for pc in self])
      
   def multiply(self, n):
      return NumericPitchClassSegment([pc.multiply(n) for pc in self])

   def retrograde(self):
      return NumericPitchClassSegment(reversed(self))

   def rotate(self, n):
      from abjad.tools import listtools
      pitch_classes = listtools.rotate(self.pitch_classes, n)
      return NumericPitchClassSegment(pitch_classes)
      
   def transpose(self, n):
      return NumericPitchClassSegment([pc.transpose(n) for pc in self])
