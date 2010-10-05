def is_diatonic_pitch_class_number(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` is a diatonic pitch class number. Otherwise false::

      abjad> pitchtools.is_diatonic_pitch_class_number(0)
      True
   
   The diatonic pitch-class numbers are equal to the set ``[0, 1, 2, 3, 4, 5, 6]``.
   '''

   if expr in range(7):
      return True
   return False
