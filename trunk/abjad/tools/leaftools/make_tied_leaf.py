from abjad.tools import durationtools
from abjad.tools import mathtools


def make_tied_leaf(kind, duration, decrease_durations_monotonically=True,
    forbidden_written_duration=None, pitches=None, tie_parts=True):
    r'''.. versionadded:: 1.0

    Example 1. Make note:

    ::

        >>> leaves = leaftools.make_tied_leaf(notetools.Note, Duration(1, 2), pitches='C#5')
        >>> staff = Staff(leaves)
        >>> time_signature = contexttools.TimeSignatureMark((2, 4))(staff)

    ::

        >>> f(staff)
        \new Staff {
            \time 2/4
            cs''2
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 2. Make note and forbid half notes:

    ::

        >>> leaves = leaftools.make_tied_leaf(
        ...     notetools.Note, Duration(1, 2), pitches='C#5',
        ...     forbidden_written_duration=Duration(1, 2))
        >>> staff = Staff(leaves)
        >>> time_signature = contexttools.TimeSignatureMark((2, 4))(staff)

    ::

        >>> f(staff)
        \new Staff {
            \time 2/4
            cs''4 ~
            cs''4
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 3. Make tied note with half notes forbidden and durations decreasing monotonically:

    ::

        >>> leaves = leaftools.make_tied_leaf(
        ...     notetools.Note, Duration(9, 8), pitches='C#5',
        ...     forbidden_written_duration=Duration(1, 2),
        ...     decrease_durations_monotonically=True)
        >>> staff = Staff(leaves)
        >>> time_signature = contexttools.TimeSignatureMark((9, 8))(staff)

    ::

        >>> f(staff)
        \new Staff {
            \time 9/8
            cs''4 ~
            cs''4 ~
            cs''4 ~
            cs''4 ~
            cs''8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 4. Make tied note with half notes forbidden and durations increasing monotonically:

    ::

        >>> leaves = leaftools.make_tied_leaf(
        ...     notetools.Note, Duration(9, 8), pitches='C#5',
        ...     forbidden_written_duration=Duration(1, 2),
        ...     decrease_durations_monotonically=False)
        >>> staff = Staff(leaves)
        >>> time_signature = contexttools.TimeSignatureMark((9, 8))(staff)

    ::

        >>> f(staff)
        \new Staff {
            \time 9/8
            cs''8 ~
            cs''4 ~
            cs''4 ~
            cs''4 ~
            cs''4
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Return list of leaves.
    '''
    from abjad.tools import tietools

    # check input
    duration = durationtools.Duration(duration)
    if forbidden_written_duration is not None:
        forbidden_written_duration = durationtools.Duration(forbidden_written_duration)
        assert forbidden_written_duration.is_assignable
        assert forbidden_written_duration.numerator == 1

    # find preferred numerator of written durations if necessary
    if forbidden_written_duration is not None and forbidden_written_duration <= duration:
        denominators = [2 * forbidden_written_duration.denominator, duration.denominator]
        denominator = mathtools.least_common_multiple(*denominators)
        forbidden_written_duration = mathtools.NonreducedFraction(forbidden_written_duration)
        forbidden_written_duration = forbidden_written_duration.with_denominator(denominator)
        duration = mathtools.NonreducedFraction(duration).with_denominator(denominator)
        forbidden_numerator = forbidden_written_duration.numerator
        assert forbidden_numerator % 2 == 0
        preferred_numerator = forbidden_numerator / 2

    # make written duration numerators
    numerators = []
    parts = mathtools.partition_integer_into_canonic_parts(duration.numerator)
    if forbidden_written_duration is not None and forbidden_written_duration <= duration:
        for part in parts:
            if forbidden_numerator <= part:
                better_parts = mathtools.partition_integer_into_parts_less_than_double(
                    part, preferred_numerator)
                numerators.extend(better_parts)
            else:
                numerators.append(part)
    else:
        numerators = parts

    # reverse numerators if necessary
    if not decrease_durations_monotonically:
        numerators = list(reversed(numerators))

    # make one leaf per written duration
    result = []
    for numerator in numerators:
        written_duration = durationtools.Duration(numerator, duration.denominator)
        if not pitches is None:
            args = (pitches, written_duration)
        else:
            args = (written_duration, )
        result.append(kind(*args))

    # apply tie spanner if required
    if tie_parts and 1 < len(result):
        tietools.TieSpanner(result)

    # return result
    return result
