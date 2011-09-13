from abjad.tools.pitchtools.is_harmonic_diatonic_interval_abbreviation import harmonic_diatonic_interval_abbreviation_regex_body
import re


melodic_diatonic_interval_abbreviation_regex_body = '''
    ([+,-]?)  # one plus, one minus, or neither
    %s             # followed by harmonic diatonic interval abbreviation
    ''' % harmonic_diatonic_interval_abbreviation_regex_body

melodic_diatonic_interval_abbreviation_regex = re.compile(
    '^%s$' % melodic_diatonic_interval_abbreviation_regex_body, re.VERBOSE)

def is_melodic_diatonic_interval_abbreviation(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a melodic diatonic interval abbreviation. Otherwise false::

        abjad> pitchtools.is_melodic_diatonic_interval_abbreviation('+M9')
        True

    The regex ``^([+,-]?)(M|m|P|aug|dim)(\d+)$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(melodic_diatonic_interval_abbreviation_regex.match(expr))
