from abjad.tools.pitchtools.IntervalClass import IntervalClass


class IntervalClassSegment(list):
   '''.. versionadded:: 1.1.2

   Ordered collection of interval class instances.
   '''

   def __init__(self, interval_class_tokens):
      interval_classes = [IntervalClass(x) for x in interval_class_tokens]
      self.extend(interval_classes)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])
