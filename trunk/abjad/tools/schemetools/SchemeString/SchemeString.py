from abjad.core import _StrictComparator


class SchemeString(_StrictComparator):
   '''Abjad model of Scheme string:

   ::

      abjad> schemetools.SchemeString('grace')
      SchemeString('grace')
   '''

   def __init__(self, string):
      self._string = string

   ## OVERLOADS ##

   def __repr__(self):
      return "%s('%s')" % (self.__class__.__name__, self._string)

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def format(self):
      '''LilyPond input format of Scheme string:

      ::

         abjad> scheme_string = schemetools.SchemeString('grace')
         abjad> scheme_string.format
         '#"grace"'
      '''
      return '#"%s"' % self._string
