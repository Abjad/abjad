from abjad.core import _StrictComparator


class SchemeString(_StrictComparator):
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
