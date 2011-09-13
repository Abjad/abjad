import re


numbered_body_strings = '|'.join([str(2 ** n) for n in range(8)])
named_body_strings = '|'.join([r'\\breve', r'\\longa', r'\\maxima'])

lilypond_duration_string_regex_body = """
    (                                    # exactly one body string equal to either
        %s     # one numbered body string
        |                                # or
        %s # one named body string
    )
    \s*                                 # zero or more whitespace characters
    (\\.*)                              # zero or more dots
    \s*                                 # zero or more whitespace characters
    (                                    # at most one lilypond multiplier string equal to
        \*                             # exactly one asterisk
        \s*                            # zero or more whitespace characters
        (                                # exactly one fraction string equal to
            \d+                         # one or more digits
            (                           # at most one denominator string equal to
                /                      # exactly one forward slash
                \d+                    # one or more digits
            )?
        )
    )?
    """ % (numbered_body_strings, named_body_strings)

#print lilypond_duration_string_regex_body

lilypond_duration_string_regex = re.compile('^%s$' %
    lilypond_duration_string_regex_body, re.VERBOSE)

def is_lilypond_duration_string(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a LilyPond duration string::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.is_lilypond_duration_string('4.. * 1/2')
        True

    Otherwise false::

        abjad> durationtools.is_lilypond_duration_string('foo')
        False

    The regex ``^(1|2|4|8|16|32|64|128|\\breve|\\longa|\\maxima)\s*(\.*)\s*(\*\s*(\d+(/\d+)?))?$``
    underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    #groups = lilypond_duration_string_regex.match(expr).groups()
    #print groups
    #base, dots, multiplier = groups[0], groups[1], groups[3]
    #print base, dots, multiplier

    return bool(lilypond_duration_string_regex.match(expr))
