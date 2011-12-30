from abjad.tools.pitchtools.is_alphabetic_accidental_abbreviation import alphabetic_accidental_regex_body
from abjad.tools.pitchtools.is_diatonic_pitch_class_name import diatonic_pitch_class_name_regex_body
import re


chromatic_pitch_class_name_regex_body = '''
    %s                # exactly one diatonic pitch-class name
    %s                # followed by exactly one alphabetic accidental name
    ''' % (diatonic_pitch_class_name_regex_body,
        alphabetic_accidental_regex_body)

chromatic_pitch_class_name_regex = re.compile(
    '^%s$' % chromatic_pitch_class_name_regex_body, re.VERBOSE)

def is_chromatic_pitch_class_name(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a chromatic pitch-class name. Otherwise false::

        abjad> pitchtools.is_chromatic_pitch_class_name('fs')
        True

    The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[fs]|)!?)$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(chromatic_pitch_class_name_regex.match(expr))
