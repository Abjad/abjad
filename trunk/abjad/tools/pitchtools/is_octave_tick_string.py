import re


octave_tick_regex_body = """
    (,+             # one or more commas for octaves below the bass clef
    |'+             # or one or more apostrophes for the octave of the treble clef
    |)              # or empty string for the octave of the bass clef
    """

octave_tick_regex = re.compile('^%s$' % octave_tick_regex_body, re.VERBOSE)

def is_octave_tick_string(expr):
    '''.. versionadded:: 2.0

    True when `expr` is an octave tick string. Otherwise false::

        abjad> pitchtools.is_octave_tick_string(',,,')
        True

    The regex ``^,+|'+|$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(octave_tick_regex.match(expr))
