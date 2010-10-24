from abjad.tools.pitchtools._PitchClassSet import _PitchClassSet
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools import listtools
from abjad.tools.pitchtools.InversionEquivalentDiatonicIntervalClassVector import InversionEquivalentDiatonicIntervalClassVector
from abjad.tools.pitchtools.NumberedChromaticPitchClassSet import NumberedChromaticPitchClassSet
from abjad.tools.pitchtools.NamedChromaticPitchClass import NamedChromaticPitchClass
from abjad.tools.pitchtools.list_harmonic_diatonic_intervals_in_expr import list_harmonic_diatonic_intervals_in_expr
from abjad.tools.pitchtools.list_numeric_chromatic_pitch_classes_in_expr import list_numeric_chromatic_pitch_classes_in_expr


class NamedChromaticPitchClassSet(_PitchClassSet):
   '''.. versionadded:: 1.1.2

   The Abjad model of a named chromatic pitch-class set::

      abjad> pitchtools.NamedChromaticPitchClassSet(['gs', 'g', 'as', 'c', 'cs'])
      NamedChromaticPitchClassSet(['as', 'c', 'cs', 'g', 'gs'])

   Named chromatic pitch-class sets are immutable.
   '''

   def __new__(self, expr):
      npcs = [ ]
      ## assume expr is iterable
      try:
         for x in expr:
            try:
               npcs.append(NamedChromaticPitchClass(x))
            except TypeError:
               ## TODO: probably fix next line ##
               npcs.extend(get_pitch_classes(x))
      ## if expr is not iterable
      except TypeError:
         ## assume expr can be turned into a single pc
         try:
            npc = NamedChromaticPitchClass(expr)
            npcs.append(npc)
         ## expr is a Rest or non-PC type
         except TypeError:
            npcs = [ ]
      return frozenset.__new__(self, npcs)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, NamedChromaticPitchClassSet):
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
      return '%s([%s])' % (self.__class__.__name__, self._repr_string)
   
   def __str__(self):
      return '{%s}' % self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      #return ', '.join([str(x) for x in sorted(self)])
      return ', '.join([str(x) for x in self._sort_self( )])

   @property
   def _repr_string(self):
      #return ', '.join([repr(str(x)) for x in sorted(self)])
      return ', '.join([repr(str(x)) for x in self._sort_self( )])

   ## PRIVATE METHODS ##

   def _sort_self(self):
      def helper(x, y):
         if x._diatonic_pitch_class_name == y._diatonic_pitch_class_name:
            return cmp(abs(x.numbered_chromatic_pitch_class), abs(y.numbered_chromatic_pitch_class))
         else:
            return cmp(x._diatonic_pitch_class_name, y._diatonic_pitch_class_name)
      result = list(self)
      result.sort(helper)
      return result
   
   ## PUBLIC ATTRIBUTES ##

   @property
   def diatonic_interval_class_vector(self):
      pitches = [NamedChromaticPitch(x, 4) for x in self]
      return InversionEquivalentDiatonicIntervalClassVector(pitches)

   @property
   def named_chromatic_pitch_classes(self):
      result = list(self)
      #return tuple(sorted(self))
      return tuple(self._sort_self( ))

   @property
   def pitch_class_set(self):
      return NumberedChromaticPitchClassSet(self)

   @property
   def pitch_classes(self):
      return self.pitch_class_set.pitch_classes

   ## PUBLIC METHODS ##
   
   def order_by(self, npc_seg):
      from abjad.tools.pitchtools.NamedChromaticPitchClassSegment import NamedChromaticPitchClassSegment
      if not len(self) == len(npc_seg):
         raise ValueError('set and segment must be of equal length.')
      for npcs in listtools.yield_all_permutations_of_iterable(self.named_chromatic_pitch_classes):
         candidate_npc_seg = NamedChromaticPitchClassSegment(npcs)
         if candidate_npc_seg.is_equivalent_under_transposition(npc_seg):
            return candidate_npc_seg
      message = 'named pitch-class set %s can not order by '
      message += 'named pitch-class segment %s.'
      raise ValueError(message % (self, npc_seg))

   def transpose(self, melodic_diatonic_interval):
      '''Transpose all npcs in self by melodic diatonic interval.'''
      return NamedChromaticPitchClassSet([
         npc + melodic_diatonic_interval for npc in self])
