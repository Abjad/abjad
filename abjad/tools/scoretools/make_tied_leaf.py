# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools.topleveltools import attach


def make_tied_leaf(
    class_,
    duration,
    decrease_durations_monotonically=True,
    forbidden_written_duration=None,
    pitches=None,
    tie_parts=True,
    use_messiaen_style_ties=False,
    ):
    r'''Makes tied `class_` with `duration`.

    ::

        >>> import abjad

    ..  container:: example

        Makes note:

        ::

            >>> leaves = abjad.scoretools.make_tied_leaf(
            ...     abjad.Note,
            ...     abjad.Duration(1, 2),
            ...     pitches='C#5',
            ...     )
            >>> staff = abjad.Staff(leaves)
            >>> time_signature = abjad.TimeSignature((2, 4))
            >>> abjad.attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \time 2/4
                cs''2
            }

    ..  container:: example

        Makes note and forbid half notes:

        ::

            >>> leaves = abjad.scoretools.make_tied_leaf(
            ...     abjad.Note,
            ...     abjad.Duration(1, 2),
            ...     pitches='C#5',
            ...     forbidden_written_duration=abjad.Duration(1, 2),
            ...     )
            >>> staff = abjad.Staff(leaves)
            >>> time_signature = abjad.TimeSignature((2, 4))
            >>> abjad.attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \time 2/4
                cs''4 ~
                cs''4
            }

    ..  container:: example

        Makes tied note with half notes forbidden and durations decreasing
        monotonically:

        ::

            >>> leaves = abjad.scoretools.make_tied_leaf(
            ...     abjad.Note,
            ...     abjad.Duration(9, 8),
            ...     pitches='C#5',
            ...     forbidden_written_duration=abjad.Duration(1, 2),
            ...     decrease_durations_monotonically=True,
            ...     )
            >>> staff = abjad.Staff(leaves)
            >>> time_signature = abjad.TimeSignature((9, 8))
            >>> abjad.attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \time 9/8
                cs''4 ~
                cs''4 ~
                cs''4 ~
                cs''4 ~
                cs''8
            }

    ..  container:: example

        Makes tied note with half notes forbidden and durations increasing
        monotonically:

        ::

            >>> leaves = abjad.scoretools.make_tied_leaf(
            ...     abjad.Note,
            ...     abjad.Duration(9, 8),
            ...     pitches='C#5',
            ...     forbidden_written_duration=abjad.Duration(1, 2),
            ...     decrease_durations_monotonically=False,
            ...     )
            >>> staff = abjad.Staff(leaves)
            >>> time_signature = abjad.TimeSignature((9, 8))
            >>> abjad.attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \time 9/8
                cs''8 ~
                cs''4 ~
                cs''4 ~
                cs''4 ~
                cs''4
            }

    ..  container:: example

        Uses Messiaen-style ties:

        ::

            >>> leaves = abjad.scoretools.make_tied_leaf(
            ...     abjad.Note,
            ...     abjad.Duration(9, 8),
            ...     pitches='C#5',
            ...     decrease_durations_monotonically=False,
            ...     forbidden_written_duration=abjad.Duration(1, 2),
            ...     use_messiaen_style_ties=True,
            ...     )
            >>> staff = abjad.Staff(leaves)
            >>> time_signature = abjad.TimeSignature((9, 8))
            >>> abjad.attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \time 9/8
                cs''8
                cs''4 \repeatTie
                cs''4 \repeatTie
                cs''4 \repeatTie
                cs''4 \repeatTie
            }

    Returns selection of leaves.
    '''
    from abjad.tools import scoretools
    from abjad.tools import spannertools

    # check input
    duration = durationtools.Duration(duration)
    if forbidden_written_duration is not None:
        forbidden_written_duration = \
            durationtools.Duration(forbidden_written_duration)
        assert forbidden_written_duration.is_assignable
        assert forbidden_written_duration.numerator == 1

    # find preferred numerator of written durations if necessary
    if (forbidden_written_duration is not None and
        forbidden_written_duration <= duration):
        denominators = [
            2 * forbidden_written_duration.denominator,
            duration.denominator,
            ]
        denominator = mathtools.least_common_multiple(*denominators)
        forbidden_written_duration = \
            mathtools.NonreducedFraction(forbidden_written_duration)
        forbidden_written_duration = \
            forbidden_written_duration.with_denominator(denominator)
        duration = mathtools.NonreducedFraction(duration)
        duration = duration.with_denominator(denominator)
        forbidden_numerator = forbidden_written_duration.numerator
        assert forbidden_numerator % 2 == 0
        preferred_numerator = forbidden_numerator / 2

    # make written duration numerators
    numerators = []
    parts = mathtools.partition_integer_into_canonic_parts(duration.numerator)
    if (forbidden_written_duration is not None and
        forbidden_written_duration <= duration):
        for part in parts:
            if forbidden_numerator <= part:
                better_parts = \
                    mathtools.partition_integer_into_parts_less_than_double(
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
        written_duration = durationtools.Duration(
            numerator,
            duration.denominator,
            )
        if not pitches is None:
            arguments = (pitches, written_duration)
        else:
            arguments = (written_duration, )
        result.append(class_(*arguments))

    # apply tie spanner if required
    if tie_parts and 1 < len(result):
        if not issubclass(class_, (scoretools.Rest, scoretools.Skip)):
            tie = spannertools.Tie(
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
            attach(tie, result)

    # return result
    result = selectiontools.Selection(result)
    return result
