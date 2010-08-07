from abjad.core import Rational


class InversionEquivalentChromaticIntervalClass(object):
   '''.. versionadded:: 1.1.2

   Inversion-equivalent interval class.
   '''

   def __init__(self, interval_class_token):
      if isinstance(interval_class_token, InversionEquivalentChromaticIntervalClass):
         self._number = interval_class_token.number
      elif isinstance(interval_class_token, (int, float, long, Rational)):
         if not 0 <= interval_class_token <= 6:
            raise ValueError('must be between 0 and 6, inclusive.')
         self._number = interval_class_token
      else:
         raise TypeError('must be interval class instance or number.')
   
   ## OVERLOADS ##

   def __abs__(self):
      return InversionEquivalentChromaticIntervalClass(abs(self.number))

   def __copy__(self):
      return InversionEquivalentChromaticIntervalClass(self.number)

   def __eq__(self, arg):
      if isinstance(arg, InversionEquivalentChromaticIntervalClass):
         if self.number == arg.number:
            return True
      return False

   def __hash__(self):
      return hash(repr(self))

   def __ne__(self, arg):
      return not self == arg

   def __neg__(self):
      return InversionEquivalentChromaticIntervalClass(self.number)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '%s' % self.number

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return self.number

   ## PUBLIC ATTRIBUTES ##

   @property
   def number(self):
      return self._number
