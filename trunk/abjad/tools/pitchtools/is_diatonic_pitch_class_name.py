import re


diatonic_pitch_class_name_regex_body = """
    ([a-g,A-G])  # exactly one lowercase a - g or uppercase A - G
    """

diatonic_pitch_class_name_regex = re.compile('^%s$' %
    diatonic_pitch_class_name_regex_body, re.VERBOSE)

def is_diatonic_pitch_class_name(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a diatonic pitch-class name. Otherwise false::

        abjad> pitchtools.is_diatonic_pitch_class_name('c')
        True

    The regex ``^[a-g,A-G]$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(diatonic_pitch_class_name_regex.match(expr))
