from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass
from abjad.tools.pitchtools.NumberedChromaticPitchClassSegment import NumberedChromaticPitchClassSegment


class TwelveToneRow(NumberedChromaticPitchClassSegment):
   '''.. versionadded:: 1.1.2

   Abjad model of twelve-tone row::

      abjad> pitchtools.TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])
      TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])

   Twelve-tone rows validate pitch-classes at initialization.

   Twelve-tone rows inherit canonical operators from numbered chromatic pitch-class segment.

   Twelve-tone rows return numbered chromatic pitch-class segments on calls to getslice.

   Twelve-tone rows are immutable.
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

   def __getslice__(self, start, stop):
      return NumberedChromaticPitchClassSegment(tuple.__getslice__(self, start, stop))

   def __eq__(self, arg):
      if isinstance(arg, TwelveToneRow):
         return tuple(self) == tuple(arg)
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s([%s])' % (self.__class__.__name__, self._contents_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_string(self):
      return ', '.join([str(abs(pc)) for pc in self])
