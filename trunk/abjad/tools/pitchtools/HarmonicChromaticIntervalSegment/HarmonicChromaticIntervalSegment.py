from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment
from abjad.tools.pitchtools.HarmonicChromaticInterval import \
   HarmonicChromaticInterval


class HarmonicChromaticIntervalSegment(_IntervalSegment):
   '''.. versionadded:: 1.1.2

   '''

   def __init__(self, hci_tokens):
      for token in hci_tokens:
         hci = HarmonicChromaticInterval(token)
         self.append(hci)
