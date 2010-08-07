from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools.pitchtools.MelodicDiatonicInterval import \
   MelodicDiatonicInterval
from abjad.tools.pitchtools.NamedPitchClass import NamedPitchClass
from abjad.tools.pitchtools.NamedPitchClassSet import NamedPitchClassSet
from abjad.tools.pitchtools.NumericPitchClassSegment import NumericPitchClassSegment
from abjad.tools.pitchtools.NumericPitchClassSet import NumericPitchClassSet
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
   def diatonic_interval_class_segment(self):
      from abjad.tools import listtools
      from abjad.tools.pitchtools.DiatonicIntervalClassSegment import \
         DiatonicIntervalClassSegment
      dics = listtools.difference_series(self)
      return DiatonicIntervalClassSegment(dics)

   @property
   def named_pitch_class_set(self):
      return NamedPitchClassSet(self)

   @property
   def named_pitch_classes(self):
      return tuple(self[:])

   @property
   def pitch_class_segment(self):
      return NumericPitchClassSegment(self)

   @property
   def pitch_class_set(self):
      return NumericPitchClassSet(self)

   @property
   def pitch_classes(self):
      return self.pitch_class_segment.pitch_classes

   ## PUBLIC METHODS ##

   def is_equivalent_under_transposition(self, arg):
      if not isinstance(arg, type(self)):
         return False
      if not len(self) == len(arg):
         return False
      difference = -(NamedPitch(arg[0], 4) - NamedPitch(self[0], 4))
      new_npcs = [x + difference for x in self]
      new_npc_seg = NamedPitchClassSegment(new_npcs)
      return arg == new_npc_seg

   def retrograde(self):
      return NamedPitchClassSegment(reversed(self))

   def rotate(self, n):
      from abjad.tools import listtools
      named_pitch_classes = listtools.rotate(self.named_pitch_classes, n)
      return NamedPitchClassSegment(named_pitch_classes)
      
   def transpose(self, melodic_diatonic_interval):
      return NamedPitchClassSegment([
         npc + melodic_diatonic_interval  for npc in self])
