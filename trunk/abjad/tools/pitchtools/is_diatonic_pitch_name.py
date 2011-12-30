from abjad.tools.pitchtools.is_diatonic_pitch_class_name import diatonic_pitch_class_name_regex_body
from abjad.tools.pitchtools.is_octave_tick_string import octave_tick_regex_body
import re


diatonic_pitch_name_regex_body = """
    %s                 # exactly one diatonic pitch-class name
    %s                 # followed by exactly one octave tick string
    """ % (diatonic_pitch_class_name_regex_body, octave_tick_regex_body)

diatonic_pitch_name_regex = re.compile(
    '^%s$' % diatonic_pitch_name_regex_body, re.VERBOSE)

def is_diatonic_pitch_name(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a diatonic pitch name. Otherwise false::

        abjad> pitchtools.is_diatonic_pitch_name("c''")
        True

    The regex ``(^[a-g,A-G])(,+|'+|)$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(diatonic_pitch_name_regex.match(expr))
