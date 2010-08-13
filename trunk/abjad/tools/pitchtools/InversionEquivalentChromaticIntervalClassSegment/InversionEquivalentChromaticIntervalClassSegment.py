from abjad.tools.pitchtools._IntervalClassSegment import _IntervalClassSegment
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClass import InversionEquivalentChromaticIntervalClass


class InversionEquivalentChromaticIntervalClassSegment(_IntervalClassSegment):
   '''.. versionadded:: 1.1.2

   Ordered collection of interval class instances.
   '''

   #def __init__(self, interval_class_tokens):
   def __new__(self, interval_class_tokens):
      interval_classes = [IntervalClass(x) for x in interval_class_tokens]
      #self.extend(interval_classes)
      return tuple.__new__(self, interval_classes)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])
