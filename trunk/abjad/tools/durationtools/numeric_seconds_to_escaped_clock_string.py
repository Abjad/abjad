import fractions


def numeric_seconds_to_escaped_clock_string(seconds):
    r'''.. versionadded:: 2.0

    Change numeric `seconds` to escaped clock string::

        >>> from abjad.tools import durationtools

    ::

        >>> note = Note("c'4")
        >>> clock_string = durationtools.numeric_seconds_to_escaped_clock_string(117)

    ::

        >>> markuptools.Markup('"%s"' % clock_string, Up)(note)
        Markup(('1\'57\\"',), direction=Up)(c'4)

    ::

        >>> f(note)
        c'4 ^ \markup { 1'57\\" }

    Escape seconds indicator for output as LilyPond markup.

    Return string.
    '''

    assert isinstance(seconds, (int, float, fractions.Fraction))
    if seconds < 0:
        raise ValueError('total seconds must be positive.')

    minutes = int(seconds / 60)
    remaining_seconds = str(int(seconds - minutes * 60)).zfill(2)
    clock_string = "%s'%s\\\"" % (minutes, remaining_seconds)

    return clock_string
