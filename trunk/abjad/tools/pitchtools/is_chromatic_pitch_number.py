def is_chromatic_pitch_number(expr):
   '''.. versionadded:: 1.1.2

   True `expr` is a chromatic pitch number. Otherwise false::

      abjad> pitchtools.is_chromatic_pitch_number(13)
      True

   The chromatic pitch numbers are equal to the set of all integers in union
   with the set of all integers plus of minus ``0.5``.
   '''

   if isinstance(expr, (int, long, float)):
      return expr % 0.5 == 0
   return False
