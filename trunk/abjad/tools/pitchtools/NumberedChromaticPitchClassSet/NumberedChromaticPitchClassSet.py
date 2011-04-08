from abjad.tools.pitchtools._PitchClassSet import _PitchClassSet
from abjad.tools import seqtools
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClassSet import InversionEquivalentChromaticIntervalClassSet
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClassVector import InversionEquivalentChromaticIntervalClassVector
from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass
from abjad.tools.pitchtools.list_numeric_chromatic_pitch_classes_in_expr import list_numeric_chromatic_pitch_classes_in_expr


class  NumberedChromaticPitchClassSet(_PitchClassSet):
   '''.. versionadded:: 1.1.2

   Abjad model of a numbered chromatic pitch-class set::

      abjad> pitchtools.NumberedChromaticPitchClassSet([-2, -1.5, 6, 7, -1.5, 7])
      NumberedChromaticPitchClassSet([6, 7, 10, 10.5])

   Numbered chromatic pitch-class sets are immutable.
   '''

   def __new__(self, expr):
      pcs = [ ]
      ## assume expr is iterable
      try:
         for x in expr:
            try:
               pcs.append(NumberedChromaticPitchClass(x))
            except TypeError:
               pcs.extend(get_pitch_classes(x))
      ## if expr is not iterable
      except TypeError:
         ## assume expr can be turned into a single pc
         try:
            pc = NumberedChromaticPitchClass(expr)
            pcs.append(pc)
         ## expr is a Rest or non-PC type
         except TypeError:
            pcs = [ ]
      #return frozenset.__new__(PitchClassSet, pcs)
      return frozenset.__new__(self, pcs)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
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
      return '%s([%s])' % (self.__class__.__name__, self._format_string)
   
   def __str__(self):
      return '{%s}' % self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      result = list(self)
      result.sort(lambda x, y: cmp(abs(x), abs(y)))
      #return ', '.join([str(x) for x in sorted(self)])
      return ', '.join([str(x) for x in result])

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class_set(self):
      #interval_class_set = InversionEquivalentChromaticIntervalClassSet([ ])
      interval_class_set = set([ ])
      for first_pc, second_pc in seqtools.yield_all_unordered_pairs_of_sequence(self):
         interval_class = first_pc - second_pc
         interval_class_set.add(interval_class)
      interval_class_set = InversionEquivalentChromaticIntervalClassSet(interval_class_set)
      return interval_class_set

   @property
   def interval_class_vector(self):
      interval_classes = [ ]
      for first_pc, second_pc in seqtools.yield_all_unordered_pairs_of_sequence(self):
         interval_class = first_pc - second_pc
         interval_classes.append(interval_class)
      return InversionEquivalentChromaticIntervalClassVector(interval_classes)

   @property
   def pitch_classes(self):
      result = list(self)
      result.sort(lambda x, y: cmp(abs(x), abs(y)))
      #return tuple(sorted(self))
      return tuple(result)

   @property
   def prime_form(self):
      '''To be implemented.'''
      return None

   ## PUBLIC METHODS ##
   
   def invert(self):
      '''Invert all pcs in self.'''
      return type(self)([pc.invert( ) for pc in self])

   def is_transposed_subset(self, pcset):
      for n in range(12):
         if self.transpose(n).issubset(pcset):
            return True
      return False

   def is_transposed_superset(self, pcset):
      for n in range(12):
         if self.transpose(n).issuperset(pcset):
            return True
      return False

   def multiply(self, n):
      '''Transpose all pcs in self by n.'''
      return type(self)([pc.multiply(n) for pc in self])

   def transpose(self, n):
      '''Transpose all pcs in self by n.'''
      return type(self)([pc.transpose(n) for pc in self])
