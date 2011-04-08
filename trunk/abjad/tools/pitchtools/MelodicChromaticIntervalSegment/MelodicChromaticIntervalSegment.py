from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment
from abjad.tools.pitchtools.HarmonicChromaticInterval import HarmonicChromaticInterval
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.MelodicChromaticIntervalClassSegment import MelodicChromaticIntervalClassSegment
from abjad.tools.pitchtools.MelodicChromaticIntervalClassVector import MelodicChromaticIntervalClassVector
from fractions import Fraction


class MelodicChromaticIntervalSegment(_IntervalSegment):
   '''.. versionadded:: 1.1.2

   Abjad model of melodic chromatic interval segment::

      abjad> pitchtools.MelodicChromaticIntervalSegment([11, 13, 13.5, -2, 2.5])
      MelodicChromaticIntervalSegment(+11, +13, +13.5, -2, +2.5)

   Melodic chromatic interval segments are immutable.
   '''

   def __new__(self, mci_tokens):
      mcis = [ ]
      for token in mci_tokens:
         mci = MelodicChromaticInterval(token)
         mcis.append(mci)
      return tuple.__new__(self, mcis)

   ## OVERLOADS ##

   def __copy__(self):
      return type(self)(self.intervals)

   ## PUBLIC ATTRIBUTES ##

   @property
   def harmonic_chromatic_interval_segment(self):
      from abjad.tools.pitchtools.HarmonicChromaticIntervalSegment import HarmonicChromaticIntervalSegment
      return HarmonicChromaticIntervalSegment(self)

   @property
   def melodic_chromatic_interval_class_segment(self):
      return MelodicChromaticIntervalClassSegment(self)

   @property
   def melodic_chromatic_interval_numbers(self):
      return tuple([mci.number for mci in self])

   @property
   def melodic_chromatic_interval_class_vector(self):
      return MelodicChromaticIntervalClassVector(self)

   @property
   def slope(self):
      '''The slope of a melodic interval segment is the sum of its intervals
      divided by its length ::

         abjad> MelodicChromaticIntervalSegment([1, 2]).slope
         Fraction(3, 2)
      '''
      return Fraction.from_float(sum([x.number for x in self])) / len(self)

   @property
   def spread(self):
      '''The maximum harmonic interval spanned by any combination of the intervals within
      a harmonic chromatic interval segment ::

         abjad> MelodicChromaticIntervalSegment([1, 2, -3, 1, -2, 1]).spread
         HarmonicChromaticInterval(4)
         abjad> MelodicChromaticIntervalSegment([1, 1, 1, 2, -3, -2]).spread
         HarmonicChromaticInterval(5)
      '''
      current = maximum = minimum = 0
      for x in self.melodic_chromatic_interval_numbers:
         current += x
         if maximum < current:
            maximum = current
         if current < minimum:
            minimum = current
      return HarmonicChromaticInterval(maximum - minimum)
