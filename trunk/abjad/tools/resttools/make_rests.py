import numbers
from abjad.tools import durationtools


def make_rests(duration_tokens, big_endian=True, tied=False):
    r'''.. versionadded:: 1.1

    Make rests.

    Make big-endian rests::

        >>> resttools.make_rests([(5, 16), (9, 16)], big_endian=True)
        [Rest('r4'), Rest('r16'), Rest('r2'), Rest('r16')]

    Make little-endian rests::

        >>> resttools.make_rests([(5, 16), (9, 16)], big_endian=False)
        [Rest('r16'), Rest('r4'), Rest('r16'), Rest('r2')]

    Make tied rests::

        >>> voice = Voice(resttools.make_rests([(5, 16), (9, 16)], tied=True))

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

    if isinstance(duration_tokens, (numbers.Number, tuple)):
        duration_tokens = [duration_tokens]

    result = []
    for d in duration_tokens:
        result.extend(resttools.make_tied_rest(d, big_endian=big_endian, tied=tied))
    return result
