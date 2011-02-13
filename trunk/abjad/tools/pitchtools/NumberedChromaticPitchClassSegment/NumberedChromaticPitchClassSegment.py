from abjad.tools.pitchtools._PitchClassSegment import _PitchClassSegment
from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass
from abjad.tools.pitchtools.NumberedChromaticPitchClassSet import NumberedChromaticPitchClassSet
import copy


class NumberedChromaticPitchClassSegment(_PitchClassSegment):
   '''.. versionadded:: 1.1.2

   The Abjad model of a numbered chromatic pitch-class segment::

      abjad> pitchtools.NumberedChromaticPitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
      NumberedChromaticPitchClassSegment(10, 10.5, 6, 7, 10.5, 7)

   Numbered chromatic pitch-class segments are immutable.
   '''

   def __new__(self, pitch_class_tokens):
      pitch_classes = [NumberedChromaticPitchClass(x) for x in pitch_class_tokens]
      return tuple.__new__(self, pitch_classes)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s([%s])' % (self.__class__.__name__, self._repr_string)

   def __str__(self):
      return '<%s>' % self._format_string
      
   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   @property
   def _repr_string(self):
      return self._format_string

   ## PUBLIC ATTRIBUTES ##

   @property
   def inversion_equivalent_chromatic_interval_class_segment(self):
      '''New inversion-equivalent chromatic interval-class segment
      from numbered chromatic pitch-class segment::

         numbered_chromatic_pitch_class_segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
         numbered_chromatic_pitch_class_segment.inversion_equivalent_chromatic_interval_class_segment
         InversionEquivalentChromaticIntervalClassSegment(0.5, 4.5, 1, 3.5, 3.5)
      '''
      from abjad.tools import mathtools
      from abjad.tools.pitchtools import InversionEquivalentChromaticIntervalClassSegment
      interval_classes = list(mathtools.difference_series(self))
      return InversionEquivalentChromaticIntervalClassSegment(interval_classes)

   @property
   def numbered_chromatic_pitch_class_set(self):
      '''New numbered chromatic pitch-class set from numbered chromatic pitch-class segment:

      ::

         numbered_chromatic_pitch_class_segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
         numbered_chromatic_pitch_class_segment.numbered_chromatic_pitch_class_set
         NumberedChromaticPitchClassSet([6, 7, 10, 10.5])
      '''
      return NumberedChromaticPitchClassSet(self)

   ## PUBLIC METHODS ##

   def alpha(self):
      '''Morris alpha transform of numbered chromatic pitch-class segment:

      ::

         numbered_chromatic_pitch_class_segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
         numbered_chromatic_pitch_class_segment.alpha( )
         NumberedChromaticPitchClassSegment([11, 11.5, 7, 6, 11.5, 6])
      '''
      from abjad.tools import mathtools
      numbers = [ ]
      for pc in self:
         pc = abs(pc)
         is_integer = True
         if not mathtools.is_integer_equivalent_number(pc):
            is_integer = False
            fraction_part = pc - int(pc)
            pc = int(pc)
         if abs(pc) % 2 == 0:
            number = (abs(pc) + 1) % 12
         else:
            number = abs(pc) - 1
         if not is_integer:
            number += fraction_part
         numbers.append(number)
      return type(self)(numbers)

   def invert(self):
      '''Invert numbered chromatic pitch-class segment:

      ::

         numbered_chromatic_pitch_class_segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
         numbered_chromatic_pitch_class_segment.invert( )
         NumberedChromaticPitchClassSegment([2, 1.5, 6, 5, 1.5, 5])
      '''
      return type(self)([pc.invert( ) for pc in self])
      
   def multiply(self, n):
      '''Multiply numbered chromatic pitch-class segment:

      ::

         numbered_chromatic_pitch_class_segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
         numbered_chromatic_pitch_class_segment.multiply(5)
         NumberedChromaticPitchClassSegment([2, 4.5, 6, 11, 4.5, 11])
      '''
      return type(self)([pc.multiply(n) for pc in self])

   def retrograde(self):
      '''Retrograde of numbered chromatic pitch-class segment:

      ::

         numbered_chromatic_pitch_class_segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
         numbered_chromatic_pitch_class_segment.retrograde( )
         NumberedChromaticPitchClassSegment([7, 10.5, 7, 6, 10.5, 10])
      '''
      return type(self)(reversed(self))

   def rotate(self, n):
      '''Rotate numbered chromatic pitch-class segment:

      ::

         numbered_chromatic_pitch_class_segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
         numbered_chromatic_pitch_class_segment.rotate(1)
         NumberedChromaticPitchClassSegment([7, 10, 10.5, 6, 7, 10.5])
      '''
      from abjad.tools import seqtools
      pitch_classes = seqtools.rotate_sequence(tuple(self), n)
      return type(self)(pitch_classes)
      
   def transpose(self, n):
      '''Transpose numbered chromatic pitch-class segment:

      ::

         numbered_chromatic_pitch_class_segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])
         numbered_chromatic_pitch_class_segment.transpose(10)
         NumberedChromaticPitchClassSegment([8, 8.5, 4, 5, 8.5, 5])
      '''
      return type(self)([pc.transpose(n) for pc in self])
