from abjad.tools.pitchtools._PitchSet import _PitchSet
from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.NumericPitchClassSet import NumericPitchClassSet
from abjad.tools.pitchtools.list_named_pitches_in_expr import list_named_pitches_in_expr
from abjad.tools.pitchtools.transpose_pitch_by_melodic_chromatic_interval import \
   transpose_pitch_by_melodic_chromatic_interval


## TODO: Make PitchSet and PCSet both inherit for a shared base class. ##

## TODO: Make PitchSet inherit from frozenset instead of set. ##

class NamedPitchSet(_PitchSet):
   '''.. versionadded:: 1.1.2

   12-ET pitch set from American pitch-class theory.
   '''

   #def __init__(self, pitch_tokens):
   def __new__(self, pitch_tokens):
      from abjad.tools.notetools.NoteHead import NoteHead
      pitches = [ ]
      for token in pitch_tokens:
         if isinstance(token, NoteHead):
            pitch = NamedPitch(token.pitch)
            #self.add(pitch)
            pitches.append(pitch)
         else:
            pitch = NamedPitch(token)
            #self.add(pitch)
            pitches.append(pitch)
      return frozenset.__new__(self, pitches)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, NamedPitchSet):
         for element in arg:
            if element not in self:
               return False
         else:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.format_string)

   def __str__(self):
      return '{%s}' % self._str_format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def format_string(self):
      return ', '.join([str(pitch) for pitch in self.pitches])

   @property
   def _str_format_string(self):
      ## TODO: implement NumericPitchSet ##
      return ', '.join([str(pitch) for pitch in self.pitches])

   ## PUBLIC ATTRIBUTES ##

   @property
   def duplicate_pitch_classes(self):
      pitch_classes = [ ]
      duplicate_pitch_classes = [ ]
      for pitch in self:
         pitch_class = pitch.numeric_pitch_class
         if pitch_class in pitch_classes:
            duplicate_pitch_classes.append(pitch_class)
         pitch_classes.append(pitch_class)
      return NumericPitchClassSet(duplicate_pitch_classes)

   @property
   def is_pitch_class_unique(self):
      return len(self) == len(self.pitch_class_set)

   @property
   def numbers(self):
      return tuple(sorted([pitch.pitch_number for pitch in self]))

   @property
   def pitch_classes(self):
      return tuple([pitch.numeric_pitch_class for pitch in self.pitches])

   @property
   def pitch_class_set(self):
      return NumericPitchClassSet(self)
      
   @property
   def pitches(self):
      return tuple(sorted(self))

   ## PUBLIC METHODS ##

   ## TODO: Implement pitch set (axis) inversion. ##

   #def invert(self):
   #   '''Transpose all pcs in self by n.'''
   #   return PCSet([pc.invert( ) for pc in self])

   def transpose(self, n):
      '''Transpose all pcs in self by n.'''
      interval = MelodicChromaticInterval(n)
      return NamedPitchSet([transpose_by_chromatic_interval(pitch, interval) for pitch in self])
