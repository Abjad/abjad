from abjad.tools.pitchtools.is_alphabetic_accidental_string import \
   alphabetic_accidental_regex_body
from abjad.tools.pitchtools.is_diatonic_pitch_class_name_string import \
   diatonic_pitch_class_name_regex_body
from abjad.tools.pitchtools.is_octave_tick_string import octave_tick_regex_body
import re


pitch_name_regex_body = '''
   (%s)            ## exactly one diatonic pitch class name string
   (%s)            ## followed by exactly one alphabetic accidental name string
   (%s)            ## followed by exactly one octave tick string
   ''' % (diatonic_pitch_class_name_regex_body,
      alphabetic_accidental_regex_body,
      octave_tick_regex_body)

pitch_name_regex = re.compile('^%s$' % pitch_name_regex_body, re.VERBOSE)

def is_pitch_name_string_with_octave_ticks(expr):
   '''True `expr` has the form of a pitch name string::

      abjad> pitchtools.is_pitch_name_string_with_octave_ticks('c,')
      True

   False otherwise::

      abjad> pitchtools.is_pitch_name_string_with_octave_ticks('foo')
      False

   The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[f,s]|)!?)(,+|'+|)$`` 
   underlies the predicate.
   '''

   return bool(pitch_name_regex.match(expr))
