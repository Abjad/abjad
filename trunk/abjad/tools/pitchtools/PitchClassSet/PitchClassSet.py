from abjad.tools import listtools
from abjad.tools.pitchtools.IntervalClassSet import IntervalClassSet
from abjad.tools.pitchtools.IntervalClassVector import IntervalClassVector
from abjad.tools.pitchtools.PitchClass import PitchClass
from abjad.tools.pitchtools.get_pitch_classes import get_pitch_classes


## TODO: Make PitchClassSet and PitchSet both inherit ##
## from a shared base class. ##

class PitchClassSet(set):
   '''.. versionadded:: 1.1.2

   12-ET pitch-class set from American pitch-class theory.
   '''

   def __init__(self, pcs):
      try:
         self.update(pcs)
      except TypeError:
         pitch_classes = get_pitch_classes(pcs)
         self.update(pitch_classes)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, PitchClassSet):
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
   def interval_class_set(self):
      interval_class_set = IntervalClassSet([ ])
      for first_pc, second_pc in listtools.get_unordered_pairs(self):
         interval_class = first_pc - second_pc
         interval_class_set.add(interval_class)
      return interval_class_set

   @property
   def interval_class_vector(self):
      interval_classes = [ ]
      for first_pc, second_pc in listtools.get_unordered_pairs(self):
         interval_class = first_pc - second_pc
         interval_classes.append(interval_class)
      return IntervalClassVector(interval_classes)

   @property
   def pitch_classes(self):
      return tuple(sorted(self))

   @property
   def prime_form(self):
      '''To be implemented.'''
      return None

   ## PUBLIC METHODS ##
   
   def add(self, arg):
      '''Custom add to allow both pitch-classes and numbers.'''
      pitch_class = PitchClass(arg)
      set.add(self, pitch_class)

   def invert(self):
      '''Invert all pcs in self.'''
      return PitchClassSet([pc.invert( ) for pc in self])

   def multiply(self, n):
      '''Transpose all pcs in self by n.'''
      return PitchClassSet([pc.multiply(n) for pc in self])

   def transpose(self, n):
      '''Transpose all pcs in self by n.'''
      return PitchClassSet([pc.transpose(n) for pc in self])

   def update(self, arg):
      '''Custom update to allow both pitch-classes and numbers.'''
      for element in arg:
         self.add(element)
