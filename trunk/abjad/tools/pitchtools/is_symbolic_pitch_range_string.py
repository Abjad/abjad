from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex_body
from abjad.tools.pitchtools.is_pitch_class_octave_number_string import pitch_class_octave_number_regex_body
import re


symbolic_pitch_range_string_regex_body = """
    ([\[(])         # open bracket or open parenthesis
    (%s|%s|-?\d+)   # pitch indicator
    ,               # comma
    [ ]*            # any amount of whitespace
    (%s|%s|-?\d+)   # pitch indicator
    ([\])])         # close bracket or close parenthesis
    """ % (pitch_class_octave_number_regex_body, chromatic_pitch_name_regex_body, 
        pitch_class_octave_number_regex_body, chromatic_pitch_name_regex_body)

symbolic_pitch_range_string_regex = re.compile('^%s$' % symbolic_pitch_range_string_regex_body, re.VERBOSE)    
def is_symbolic_pitch_range_string(expr):
    '''.. versionadded:: 2.5

    True when `expr` is a symbolic pitch range string. Otherwise false::

        abjad> pitchtools.is_symbolic_pitch_range_string('[A0, C8]')
        True

    The regex that underlies this predicate matches against two comma-separated pitch
    indicators enclosed in some combination of square brackets and round parentheses.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(symbolic_pitch_range_string_regex.match(expr))
