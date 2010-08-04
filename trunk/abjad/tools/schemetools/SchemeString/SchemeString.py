from abjad.core import _Abjad


class SchemeString(_Abjad):
   '''Wrapper for string in Scheme.'''

   def __init__(self, string):
      self._string = string

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def format(self):
      return '#"%s"' % self.string

   @property
   def string(self):
      return self._string
