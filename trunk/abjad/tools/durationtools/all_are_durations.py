def all_are_durations(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad durations::

        >>> from abjad.tools import durationtools

    ::

        >>> durations = [Duration((3, 16)), Duration((4, 16))]

    ::

        >>> durationtools.all_are_durations(durations)
        True

    True when `expr` is an empty sequence::

        >>> durationtools.all_are_durations([])
        True

    Otherwise false::

        >>> durationtools.all_are_durations('foo')
        False

    Return boolean.
    '''
    from abjad.tools import durationtools

    return all([isinstance(x, durationtools.Duration) for x in expr])
