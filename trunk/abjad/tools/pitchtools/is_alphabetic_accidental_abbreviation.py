import re


alphabetic_accidental_regex_body = """
    ([s]{1,2}     # s or ss for sharp or double sharp
    |[f]{1,2}     # or f or ff for flat or double flat
    |t?q?[fs]     # or qs, qf, tqs, tqf for quartertone accidentals
    |                # or empty string for no natural
    )!?             # plus optional ! for forced printing of accidental
    """

alphabetic_accidental_regex = re.compile('^%s$' % alphabetic_accidental_regex_body, re.VERBOSE)

def is_alphabetic_accidental_abbreviation(expr):
    '''.. versionadded:: 2.0

    True when `expr` is an alphabetic accidental abbrevation. Otherwise false::

        abjad> pitchtools.is_alphabetic_accidental_abbreviation('tqs')
        True

    The regex ``^([s]{1,2}|[f]{1,2}|t?q?[fs])!?$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(alphabetic_accidental_regex.match(expr))
