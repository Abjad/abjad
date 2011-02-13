from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment
from abjad.tools.pitchtools.HarmonicChromaticInterval import HarmonicChromaticInterval


class HarmonicChromaticIntervalSegment(_IntervalSegment):
   '''.. versionadded:: 1.1.2

   Abjad model of harmonic chromatic interval segment::

      abjad> pitchtools.HarmonicChromaticIntervalSegment([10, -12, -13, -13.5])
      HarmonicChromaticIntervalSegment(10, 12, 13, 13.5)

   Harmonic chromatic interval segments are immutable.
   '''

   def __new__(self, hci_tokens):
      hcis = [ ]
      for token in hci_tokens:
         hci = HarmonicChromaticInterval(token)
         hcis.append(hci)
      return tuple.__new__(self, hcis)
