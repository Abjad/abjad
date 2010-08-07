from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClass import InversionEquivalentChromaticIntervalClass


class InversionEquivalentChromaticIntervalClassSet(set):
   '''.. versionadded:: 1.1.2

   Unordered collection of interval class instances.
   '''

   def __init__(self, interval_class_tokens):
      self._interval_classes = [ ] ## can this line be deleted?
      for token in interval_class_tokens:
         interval_class = InversionEquivalentChromaticIntervalClass(token)
         self.add(interval_class)

   ## OVERLOADS ##

   def __copy__(self):
      return InversionEquivalentChromaticIntervalClassSet(self.numbers)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in sorted(self.numbers)])

   ## PUBLIC ATTRIBUTES ##
      
   @property
   def interval_classes(self):
      interval_classes = list(self)
      interval_classes.sort(lambda x, y: cmp(x.number, y.number))
      return interval_classes

   @property
   def numbers(self):
      return set([interval_class.number for interval_class in self])
