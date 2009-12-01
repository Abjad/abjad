class _IntervalSegment(list):
   '''.. versionadded:: 1.1.2

   Abstract ordered collection of interval instances class from
   which concrete classes inherit.
   '''

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##
   
   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   ## PUBLIC ATTRIBUTES ##

   @property
   def intervals(self):
      return self[:]
