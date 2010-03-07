#from abjad.exceptions import DurationError
#from abjad.rational import Rational
#import re
from abjad.tools.durtools.duration_string_to_rational import \
   duration_string_to_rational


def duration_string_to_rationals(duration_string):
   '''.. versionadded:: 1.1.2

   Convert LilyPond-style `duration_string` to list of 
   zero or more rationals. ::

      abjad> durtools.duration_string_to_rationals('8.. 32 8.. 32')            
      [Rational(7, 32), Rational(1, 32), Rational(7, 32), Rational(1, 32)]
   '''

   if not isinstance(duration_string, str):
      raise TypeError('duration string must be string.')

   rationals = [ ]
   duration_strings = duration_string.split( )
   for duration_string in duration_strings:
      rational = duration_string_to_rational(duration_string)
      rationals.append(rational)
   
   return rationals 
