def is_diatonic_pitch_number(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` is a diatonic pitch number. Otherwise false::

      abjad> pitchtools.is_diatonic_pitch_number(7)
      True

   The diatonic pitch numbers are equal to the set of integers.
   '''

   return isinstance(expr, (int, long))
