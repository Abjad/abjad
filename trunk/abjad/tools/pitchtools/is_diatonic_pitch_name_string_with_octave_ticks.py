from abjad.tools.pitchtools.is_diatonic_pitch_class_name_string import \
   diatonic_pitch_class_name_regex_body
from abjad.tools.pitchtools.is_octave_tick_string import octave_tick_regex_body
import re


diatonic_pitch_name_string_with_octave_ticks_regex_body = """
   (%s)            ## exactly one diatonic pitch class name string
   (%s)            ## followed by exactly one octave tick string
   """ % (diatonic_pitch_class_name_regex_body, octave_tick_regex_body)

diatonic_pitch_name_string_with_octave_ticks_regex = re.compile(
   '^%s$' % diatonic_pitch_name_string_with_octave_ticks_regex_body, re.VERBOSE)

def is_diatonic_pitch_name_string_with_octave_ticks(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` has the form of a diatonic pitch name string with octave ticks::

      abjad> pitchtools.is_diatonic_pitch_name_string_with_octave_ticks('c,')
      True

   False otherwise::

      abjad> pitchtools.is_diatonic_pitch_name_string_with_octave_ticks('foo')
      False

   The regex ``(^[a-g,A-G])(,+|'+|)$`` underlies the predicate.
   '''

   return bool(diatonic_pitch_name_string_with_octave_ticks_regex.match(expr))
