class _IntervalClass(object):
   '''.. versionadded:: 1.1.2

   Abstract interval class class from which conrete interval classes inherit.
   '''

   ## OVERLOADS ##

   def __hash__(self):
      return hash(repr(self))
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return str(self.number)

   ## PUBLIC ATTRIBUTES ##

   @property
   def number(self):
      return self._number
