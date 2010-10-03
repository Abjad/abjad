import re


octave_tick_regex_body = """
   ,+           ## one or more commas for octaves below the bass clef
   |'+          ## or one or more apostrophes for the octave of the treble clef
   |            ## or empty string for the octave of the bass clef
   """

octave_tick_regex = re.compile('^%s$' % octave_tick_regex_body, re.VERBOSE)

def is_octave_tick_string(expr):
   '''True when `expr` has the form of an octave tick string::

      abjad> pitchtools.is_octave_tick_string(',,,')
      True

   False otherwise::

      abjad> pitchtools.is_octave_tick_string('foo')
      False

   The regex ``^,+|'+|$`` underlies the predicate.
   '''

   return bool(octave_tick_regex.match(expr))
