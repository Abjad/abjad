import re


diatonic_quality_abbreviation_regex_body = '''
    (M|         # major
    m|          # minor
    P|          # perfect
    aug|        # augmented
    dim)        # dimished
    '''

diatonic_quality_abbreviation_regex = re.compile(
    '^%s$' % diatonic_quality_abbreviation_regex_body, re.VERBOSE)

def is_diatonic_quality_abbreviation(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a diatonic quality abbreviation. Otherwise false::

        abjad> pitchtools.is_diatonic_quality_abbreviation('aug')
        True

    The regex ``^M|m|P|aug|dim$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(diatonic_quality_abbreviation_regex.match(expr))
