import fractions


def numeric_seconds_to_clock_string(seconds, escape_ticks=False):
    r'''.. versionadded:: 2.0

    Example 1. Change numeric `seconds` to clock string::

        >>> durationtools.numeric_seconds_to_clock_string(117)
        '1\'57"'

    Example 2. Change numeric `seconds` to escaped clock string::

        >>> note = Note("c'4")
        >>> clock_string = durationtools.numeric_seconds_to_clock_string(117, escape_ticks=True)

    ::

        >>> markuptools.Markup('"%s"' % clock_string, Up)(note)
        Markup(('1\'57\\"',), direction=Up)(c'4)

    ::

        >>> f(note)
        c'4 ^ \markup { 1'57\\" }

    Return string.
    '''

    assert isinstance(seconds, (int, float, fractions.Fraction))
    if seconds < 0:
        raise ValueError('total seconds must be positive.')

    minutes = int(seconds / 60)
    remaining_seconds = str(int(seconds - minutes * 60)).zfill(2)
    if escape_ticks:
        clock_string = "%s'%s\\\"" % (minutes, remaining_seconds)
    else:
        clock_string = "%s'%s\"" % (minutes, remaining_seconds)

    return clock_string
