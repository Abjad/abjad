from abjad.tools.pitchtools.NamedPitchClass import NamedPitchClass
from abjad.tools.pitchtools.NamedPitchClassSet import NamedPitchClassSet
from abjad.tools.pitchtools.PitchClassSegment import PitchClassSegment
from abjad.tools.pitchtools.PitchClassSet import PitchClassSet
import copy


class NamedPitchClassSegment(list):
   '''.. versionadded:: 1.1.2

   Ordered collection of named pitch-class instances.
   '''

   def __init__(self, named_pitch_class_tokens):
      npcs = [NamedPitchClass(x) for x in named_pitch_class_tokens]
      self.extend(npcs)

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
   def named_pitch_class_set(self):
      return NamedPitchClassSet(self)

   @property
   def named_pitch_classes(self):
      return tuple(self[:])

   @property
   def pitch_class_segment(self):
      return PitchClassSegment(self)

   @property
   def pitch_class_set(self):
      return PitchClassSet(self)

   @property
   def pitch_classes(self):
      return self.pitch_class_segment.pitch_classes

   ## PUBLIC METHODS ##

   def retrograde(self):
      return NamedPitchClassSegment(reversed(self))

   def rotate(self, n):
      from abjad.tools import listtools
      named_pitch_classes = listtools.rotate(self.named_pitch_classes, n)
      return NamedPitchClassSegment(named_pitch_classes)
      
   def transpose(self, melodic_diatonic_interval):
      return NamedPitchClassSegment([
         npc + melodic_diatonic_interval  for npc in self])
