from abjad.tools.pitchtools.is_diatonic_quality_abbreviation import diatonic_quality_abbreviation_regex_body
import re


harmonic_diatonic_interval_abbreviation_regex_body = '''
    %s             # exactly one diatonic quality abbreviation
    (\d+)      # followed by one or more digits
    ''' % diatonic_quality_abbreviation_regex_body

harmonic_diatonic_interval_abbreviation_regex = re.compile(
    '^%s$' % harmonic_diatonic_interval_abbreviation_regex_body, re.VERBOSE)

def is_harmonic_diatonic_interval_abbreviation(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a harmonic diatonic interval abbreviation. Otherwise false::

        abjad> pitchtools.is_harmonic_diatonic_interval_abbreviation('M9')
        True

    The regex ``^(M|m|P|aug|dim)(\d+)$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(harmonic_diatonic_interval_abbreviation_regex.match(expr))
