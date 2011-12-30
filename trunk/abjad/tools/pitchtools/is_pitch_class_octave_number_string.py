import re


# TODO: add quartertone support
pitch_class_octave_number_regex_body = """
    ([A-G]{1,1})                      # exactly one diatonic pitch-class letter
    ([#]{0,2}|[b]{0,2})                      # plus 0 or 1 accidental names
    ([-]{0,1}                        # plus an optional negative sign
    [0-9]+)                          # plus one or more digits
    """

pitch_class_octave_number_regex = re.compile('^%s$' % pitch_class_octave_number_regex_body, re.VERBOSE)

def is_pitch_class_octave_number_string(expr):
    '''.. versionadded:: 2.5

    True when `expr` is a pitch-class / octave number string. Otherwise false::

        abjad> pitchtools.is_pitch_class_octave_number_string('C#2')
        True

    The regex ... underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(pitch_class_octave_number_regex.match(expr))
