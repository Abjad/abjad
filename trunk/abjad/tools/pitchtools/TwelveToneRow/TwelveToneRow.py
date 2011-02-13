from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass
from abjad.tools.pitchtools.NumberedChromaticPitchClassSegment import NumberedChromaticPitchClassSegment


class TwelveToneRow(NumberedChromaticPitchClassSegment):
   '''.. versionadded:: 1.1.2

   Twelve tone row.
   '''

   def __new__(self, pitch_classes):
      from abjad.tools.pitchtools.TwelveToneRow._validate_pitch_classes import \
         _validate_pitch_classes
      pitch_classes = [NumberedChromaticPitchClass(pc) for pc in pitch_classes]
      _validate_pitch_classes(pitch_classes)
      return NumberedChromaticPitchClassSegment.__new__(self, pitch_classes)

   ## OVERLOADS ##

   def __copy__(self):
      return TwelveToneRow(self)

   def __eq__(self, arg):
      if isinstance(arg, TwelveToneRow):
         return tuple(self) == tuple(arg)
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._contents_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_string(self):
      return ', '.join([str(abs(pc)) for pc in self])

   ## PUBLIC METHODS ##

   def alpha(self):
      numbers = [ ]
      for pc in self:
         if abs(pc) % 2 == 0:
            numbers.append((abs(pc) + 1) % 12)
         else:
            numbers.append(abs(pc) - 1)
      return TwelveToneRow(numbers)

   def invert(self):
      numbers = [12 - abs(pc) for pc in self]
      return TwelveToneRow(numbers)

   def reverse(self):
      return TwelveToneRow(reversed(self))

   def transpose(self, n):
      if not isinstance(n, int):
         raise TypeError
      numbers = [(abs(pc) + n) % 12 for pc in self]
      return TwelveToneRow(numbers)
