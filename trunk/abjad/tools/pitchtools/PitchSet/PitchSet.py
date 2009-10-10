from abjad.pitch import Pitch
from abjad.tools.pitchtools.ChromaticInterval import ChromaticInterval
from abjad.tools.pitchtools.transpose_by_chromatic_interval import \
   transpose_by_chromatic_interval


## TODO: Make PitchSet and PCSet both inherit for a shared base class. ##

class PitchSet(set):
   '''.. versionadded:: 1.1.2

   12-ET pitch set from American pitch-class theory.
   '''

   def __init__(self, pitches):
      self.update(pitches)

   ## OVERLOADS ##

   def __contains__(self, arg):
      if isinstance(arg, Pitch):
         for pc in self:
            if pc == arg:
               return True
      return False

   def __eq__(self, arg):
      if isinstance(arg, PitchSet):
         for element in arg:
            if element not in self:
               return False
         else:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      contents = list(self)
      contents.sort( )
      return '%s(%s)' % (self.__class__.__name__, contents)

   ## PUBLIC METHODS ##

   def add(self, arg):
      '''Built-in add( ) extended with type- and value-checking.'''
      pitch = Pitch(arg)
      if pitch not in self:
         set.add(self, pitch)

   ## TODO: Implement pitch set (axis) inversion. ##

   #def invert(self):
   #   '''Transpose all pcs in self by n.'''
   #   return PCSet([pc.invert( ) for pc in self])

   def transpose(self, n):
      '''Transpose all pcs in self by n.'''
      interval = ChromaticInterval(n)
      return PitchSet(
         [transpose_by_chromatic_interval(pitch, interval) for pitch in self])

   def update(self, arg):
      '''Built-in update( ) extended with type- and value-checking.'''
      for element in arg:
         self.add(element)
