import numbers
from abjad.tools import durationtools


def make_rests(durations, decrease_durations_monotonically=True, tie_parts=False):
    r'''.. versionadded:: 1.1

    Make rests.

    Make rests and drecrease durations monotonically::

        >>> resttools.make_rests([(5, 16), (9, 16)], decrease_durations_monotonically=True)
        [Rest('r4'), Rest('r16'), Rest('r2'), Rest('r16')]

    Makes rests and increase durations monotonically::

        >>> resttools.make_rests([(5, 16), (9, 16)], decrease_durations_monotonically=False)
        [Rest('r16'), Rest('r4'), Rest('r16'), Rest('r2')]

    Make tied rests::

        >>> voice = Voice(resttools.make_rests([(5, 16), (9, 16)], tie_parts=True))

    ::

        >>> f(voice)
        \new Voice {
            r4 ~
            r16
            r2 ~
            r16
        }

    Return list of rests.

    .. versionchanged:: 2.0
        renamed ``construct.rests()`` to
        ``resttools.make_rests()``.
    '''
    from abjad.tools import resttools

    # check input
    if isinstance(durations, (numbers.Number, tuple)):
        durations = [durations]

    # make rests
    result = []
    for duration in durations:
        result.extend(resttools.make_tied_rest(
            duration, decrease_durations_monotonically=decrease_durations_monotonically, 
            tie_parts=tie_parts))

    # return result
    return result
