from abjad.tools.pitchtools.is_chromatic_pitch_class_name import is_chromatic_pitch_class_name


def is_chromatic_pitch_class_name_octave_number_pair(expr):
   '''True when `arg` has the form of a chromatic pitch-class / octave number pair::

      abjad> pitchtools.is_chromatic_pitch_class_name_octave_number_pair(('cs', 5))
      True

   Otherwise false.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.is_pair( )`` to
      ``pitchtools.is_pitch_pair( )`` to
      ``pitchtools.is_chromatic_pitch_class_name_octave_number_pair( )``.
   '''

   if isinstance(expr, tuple):
      if len(expr) == 2:
         if is_chromatic_pitch_class_name(expr[0]):
            if isinstance(expr[1], (int, long)):
               return True
   return False
