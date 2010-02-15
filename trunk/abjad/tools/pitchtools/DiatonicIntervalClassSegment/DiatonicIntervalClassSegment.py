from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment
from abjad.tools.pitchtools.DiatonicIntervalClass import \
   DiatonicIntervalClass


class DiatonicIntervalClassSegment(_IntervalSegment):
   '''.. versionadded:: 1.1.2

   Ordered collection of diatonic interval class instances.
   '''

   def __init__(self, diatonic_interval_class_tokens):
      for token in diatonic_interval_class_tokens:
         dic = DiatonicIntervalClass(token)
         self.append(dic)

   ## OVERLOADS ##

   def __copy__(self):
      return DiatonicIntervalClassSegment(self.intervals)
