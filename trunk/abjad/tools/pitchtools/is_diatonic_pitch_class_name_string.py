import re


diatonic_pitch_class_name_string_regex = re.compile('^[a-g,A-G]$')

def is_diatonic_pitch_class_name_string(expr):
   '''True when `expr` has the form of a diatonic pitch-class name string::

      abjad> pitchtools.is_diatonic_pitch_class_name_string('a')
      True

   False otherwise::

      abjad> pitchtools.is_diatonic_pitch_class_name_string('q')
      False

   The regex ``^[a-g,A-G]$`` underlies this function.
   '''

   return bool(diatonic_pitch_class_name_string_regex.match(expr))
