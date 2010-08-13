from abjad.core import _Immutable


class _Interval(_Immutable):
   '''.. versionadded:: 1.1.2

   Abstract interval class from which concrete classes inherit.
   '''

   ## OVERLOADS ##

   def __hash__(self):
      return hash(repr(self))

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return str(self.number)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return str(self.number)

   ## PUBLIC ATTRIBUTES ##

   @property
   def cents(self):
      return 100 * self.semitones

   @property
   def interval_class(self):
      pass

   @property
   def number(self):
      return self._number

   @property
   def semitones(self):
      pass
