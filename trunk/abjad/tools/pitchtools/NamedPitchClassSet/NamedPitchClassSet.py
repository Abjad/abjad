from abjad.pitch import Pitch
from abjad.tools import listtools
#from abjad.tools.pitchtools.IntervalClassSet import IntervalClassSet
#from abjad.tools.pitchtools.IntervalClassVector import IntervalClassVector
from abjad.tools.pitchtools.DiatonicIntervalClassVector import \
   DiatonicIntervalClassVector
from abjad.tools.pitchtools.PitchClassSet import PitchClassSet
from abjad.tools.pitchtools.NamedPitchClass import NamedPitchClass
from abjad.tools.pitchtools.get_harmonic_diatonic_intervals_in import \
   get_harmonic_diatonic_intervals_in
from abjad.tools.pitchtools.get_pitch_classes import get_pitch_classes


## TODO: Make NamedPitchClassSet and PitchSet both inherit ##
## from a shared base class. ##

class NamedPitchClassSet(frozenset):
   '''.. versionadded:: 1.1.2

   Unordered set of named pitch-classes.
   '''

   def __new__(self, expr):
      npcs = [ ]
      ## assume expr is iterable
      try:
         for x in expr:
            try:
               npcs.append(NamedPitchClass(x))
            except TypeError:
               ## TODO: probably fix next line ##
               npcs.extend(get_pitch_classes(x))
      ## if expr is not iterable
      except TypeError:
         ## assume expr can be turned into a single pc
         try:
            npc = NamedPitchClass(expr)
            npcs.append(npc)
         ## expr is a Rest or non-PC type
         except TypeError:
            npcs = [ ]
      #return frozenset.__new__(NamedPitchClassSet, npcs)
      return frozenset.__new__(self, npcs)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, NamedPitchClassSet):
         for element in arg:
            if element not in self:
               return False
         else:
            return True
      return False

   def __hash__(self):
      return hash(repr(self))

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)
   
   def __str__(self):
      return '{%s}' % self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in sorted(self)])

   ## PUBLIC ATTRIBUTES ##

   @property
   def diatonic_interval_class_vector(self):
      pitches = [Pitch(x, 4) for x in self]
      return DiatonicIntervalClassVector(pitches)

#   @property
#   def interval_class_set(self):
#      interval_class_set = IntervalClassSet([ ])
#      for first_pc, second_pc in listtools.get_unordered_pairs(self):
#         interval_class = first_pc - second_pc
#         interval_class_set.add(interval_class)
#      return interval_class_set

#   @property
#   def interval_class_vector(self):
#      interval_classes = [ ]
#      for first_pc, second_pc in listtools.get_unordered_pairs(self):
#         interval_class = first_pc - second_pc
#         interval_classes.append(interval_class)
#      return IntervalClassVector(interval_classes)

   @property
   def named_pitch_classes(self):
      return tuple(sorted(self))

   @property
   def pitch_class_set(self):
      return PitchClassSet(self)

   @property
   def pitch_classes(self):
      return self.pitch_class_set.pitch_classes

   ## PUBLIC METHODS ##
   
   def order_by(self, npc_seg):
      from abjad.tools.pitchtools.NamedPitchClassSegment import \
         NamedPitchClassSegment
      if not len(self) == len(npc_seg):
         raise ValueError('set and segment must be of equal length.')
      for npcs in listtools.permutations(self.named_pitch_classes):
         candidate_npc_seg = NamedPitchClassSegment(npcs)
         if candidate_npc_seg.is_equivalent_under_transposition(npc_seg):
            return candidate_npc_seg
      message = 'named pitch-class set %s can not order by '
      message += 'named pitch-class segment %s.'
      raise ValueError(message % (self, npc_seg))

   def transpose(self, melodic_diatonic_interval):
      '''Transpose all npcs in self by melodic diatonic interval.'''
      return NamedPitchClassSet([
         npc + melodic_diatonic_interval for npc in self])
