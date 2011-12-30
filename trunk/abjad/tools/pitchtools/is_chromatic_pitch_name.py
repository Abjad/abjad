from abjad.tools.pitchtools.is_alphabetic_accidental_abbreviation import alphabetic_accidental_regex_body
from abjad.tools.pitchtools.is_diatonic_pitch_class_name import diatonic_pitch_class_name_regex_body
from abjad.tools.pitchtools.is_octave_tick_string import octave_tick_regex_body
import re


chromatic_pitch_name_regex_body = '''
    %s                 # exactly one diatonic pitch-class name
    %s                 # followed by exactly one alphabetic accidental name
    %s                 # followed by exactly one octave tick string
    ''' % (diatonic_pitch_class_name_regex_body,
        alphabetic_accidental_regex_body,
        octave_tick_regex_body)

chromatic_pitch_name_regex = re.compile('^%s$' % chromatic_pitch_name_regex_body, re.VERBOSE)

def is_chromatic_pitch_name(expr):
    '''.. versionadded:: 2.0

    True `expr` is a chromatic pitch name. Otherwise false::

        abjad> pitchtools.is_chromatic_pitch_name('c,')
        True

    The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[f,s]|)!?)(,+|'+|)$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(chromatic_pitch_name_regex.match(expr))
