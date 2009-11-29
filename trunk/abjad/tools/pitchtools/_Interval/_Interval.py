class _Interval(object):
   '''.. versionadded:: 1.1.2

   Abstract interval class from which concrete classes inherit.
   '''

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ' '

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class(self):
      pass

   @property
   def interval_number(self):
      return self._interval_number

   @property
   def semitones(self):
      pass
