import re


lilypond_duration_name_regex_body = r'''
    (\\breve|\\longa|\\maxima)    # exactly one of three duration names
    '''

lilypond_duration_name_regex = re.compile('^%s$' %
    lilypond_duration_name_regex_body, re.VERBOSE)

def is_lilypond_duration_name(expr):
    r'''.. versionadded:: 2.0

    True when `expr` is a LilyPond duartion name::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.is_lilypond_duration_name('\\breve')
        True

    Otherwise false::

        abjad> durationtools.is_lilypond_duration_name('foo')
        False

    The regex ``^(\\breve|\\longa|\\maxima)$`` underlies this predicate.

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(lilypond_duration_name_regex.match(expr))
