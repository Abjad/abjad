from abjad.tools.durationtools.is_lilypond_duration_string import lilypond_duration_string_regex_body
import re


lilypond_rest_string_regex_body = '''
    (r|R)     # either r or R followed by
    \s*        # zero or more whitespace characters followed by
    %s         # a LilyPond duration string
    ''' % (lilypond_duration_string_regex_body, )


#print lilypond_rest_string_regex_body

lilypond_rest_string_regex = re.compile('^%s$' %
    lilypond_rest_string_regex_body, re.VERBOSE)

def is_lilypond_rest_string(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a LilyPond rest string::

        abjad> resttools.is_lilypond_rest_string('r4.. * 1/2')
        True

    Otherwise false::

        abjad> resttools.is_lilypond_rest_string('text')
        False

    The regex
    ``^(r|R)\s*(1|2|4|8|16|32|64|128|\\breve|\\longa|\\maxima)\s*(\.*)\s*(\*\s*(\d+(/\d+)?))?$``
    underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(lilypond_rest_string_regex.match(expr))
