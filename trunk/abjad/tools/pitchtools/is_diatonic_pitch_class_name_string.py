import re


diatonic_pitch_class_name_regex_body = """
   [a-g,A-G]    ## exactly one lowercase a - g or uppercase A - G
   """

diatonic_pitch_class_name_regex = re.compile('^%s$' % 
   diatonic_pitch_class_name_regex_body, re.VERBOSE)

def is_diatonic_pitch_class_name_string(expr):
   '''True when `expr` has the form of a diatonic pitch-class name string::

      abjad> pitchtools.is_diatonic_pitch_class_name_string('c')
      True

   False otherwise::

      abjad> pitchtools.is_diatonic_pitch_class_name_string('q')
      False

   The regex ``^[a-g,A-G]$`` underlies the predicate.
   '''

   return bool(diatonic_pitch_class_name_regex.match(expr))
