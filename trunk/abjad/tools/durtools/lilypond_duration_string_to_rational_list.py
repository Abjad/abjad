from abjad.tools.durtools.lilypond_duration_string_to_rational import \
   lilypond_duration_string_to_rational


def lilypond_duration_string_to_rational_list(duration_string):
   '''.. versionadded:: 1.1.2

   Convert LilyPond-style `duration_string` to list of 
   zero or more rationals. ::

      abjad> durtools.lilypond_duration_string_to_rationals('8.. 32 8.. 32')            
      [Rational(7, 32), Rational(1, 32), Rational(7, 32), Rational(1, 32)]

   .. versionchanged:: 1.1.2
      renamed ``durtools.duration_string_to_rationals( )`` to
      ``durtools.lilypond_duration_string_to_rational_list( )``.
   '''

   if not isinstance(duration_string, str):
      raise TypeError('duration string must be string.')

   rationals = [ ]
   duration_strings = duration_string.split( )
   for duration_string in duration_strings:
      rational = lilypond_duration_string_to_rational(duration_string)
      rationals.append(rational)
   
   return rationals 
