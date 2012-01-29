from abjad.tools.durationtools.Duration import Duration


def all_are_durations(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad durations::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durations = [Duration((3, 16)), Duration((4, 16))]

    ::

        abjad> durationtools.all_are_durations(durations)
        True

    True when `expr` is an empty sequence::

        abjad> durationtools.all_are_durations([])
        True

    Otherwise false::

        abjad> durationtools.all_are_durations('foo')
        False

    Return boolean.
    '''

    return all([isinstance(x, Duration) for x in expr])
