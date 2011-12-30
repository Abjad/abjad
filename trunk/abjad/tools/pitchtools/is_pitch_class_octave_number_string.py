from abjad.tools.pitchtools.is_symbolic_accidental_string import symbolic_accidental_string_regex_body
import re


pitch_class_octave_number_regex_body = """
    ([A-G])         # exactly one diatonic pitch-class letter
    %s                # plus an optional symbolic accidental string
    ([-]?           # plus an optional negative sign
    [0-9]+)         # plus one or more digits
    """ % symbolic_accidental_string_regex_body

pitch_class_octave_number_regex = re.compile('^%s$' % pitch_class_octave_number_regex_body, re.VERBOSE)

def is_pitch_class_octave_number_string(expr):
    '''.. versionadded:: 2.5

    True when `expr` is a pitch-class / octave number string. Otherwise false::

        abjad> pitchtools.is_pitch_class_octave_number_string('C#2')
        True

    Quartertone accidentals are supported.

    The regex ``^([A-G])([#]{1,2}|[b]{1,2}|[#]?[+]|[b]?[~]|)([-]?[0-9]+)$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(pitch_class_octave_number_regex.match(expr))
