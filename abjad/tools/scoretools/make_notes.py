# -*- coding: utf-8 -*-
import fractions
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools


def make_notes(
    pitches,
    durations,
    decrease_durations_monotonically=True,
    use_messiaen_style_ties=False,
    ):
    r'''Makes notes according to `pitches` and `durations`.


    ..  container:: example

        **Example 1.** Cycles through `pitches` when the length of `pitches` is
        less than the length of `durations`:

        ::

            >>> notes = scoretools.make_notes([0], [(1, 16), (1, 8), (1, 8)])
            >>> notes
            Selection([Note("c'16"), Note("c'8"), Note("c'8")])

        ::

            >>> staff = Staff(notes)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'16
                c'8
                c'8
            }

    ..  container:: example

        **Example 2.** Cycles through `durations` when the length of `durations`
        is less than the length of `pitches`:

        ::

            >>> notes = scoretools.make_notes(
            ...     [0, 2, 4, 5, 7],
            ...     [(1, 16), (1, 8), (1, 8)],
            ...     )
            >>> notes
            Selection([Note("c'16"), Note("d'8"), Note("e'8"), Note("f'16"), Note("g'8")])

        ::

            >>> staff = Staff(notes)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'16
                d'8
                e'8
                f'16
                g'8
            }

    ..  container:: example

        **Example 3.** Creates ad hoc tuplets for nonassignable durations:

        ::

            >>> notes = scoretools.make_notes([0], [(1, 16), (1, 12), (1, 8)])
            >>> notes
            Selection([Note("c'16"), Tuplet(Multiplier(2, 3), "c'8"), Note("c'8")])

        ::

            >>> staff = Staff(notes)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'16
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'8
                }
                c'8
            }

    ..  container:: example

        **Example 4.** Set ``decrease_durations_monotonically=True`` to express
        tied values in decreasing duration:

        ::

            >>> notes = scoretools.make_notes(
            ...     [0],
            ...     [(13, 16)],
            ...     decrease_durations_monotonically=True,
            ...     )
            >>> notes
            Selection([Note("c'2."), Note("c'16")])

        ::

            >>> staff = Staff(notes)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'2. ~
                c'16
            }

    ..  container:: example

        **Example 5.** Set ``decrease_durations_monotonically=False`` to
        express tied values in increasing duration:

        ::

            >>> notes = scoretools.make_notes(
            ...     [0],
            ...     [(13, 16)],
            ...     decrease_durations_monotonically=False,
            ...     )
            >>> notes
            Selection([Note("c'16"), Note("c'2.")])

        ::

            >>> staff = Staff(notes)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'16 ~
                c'2.
            }

    ..  container:: example

        **Example 6.** Uses Messiaen-style ties:

        ::

            >>> notes = scoretools.make_notes(
            ...     [0],
            ...     [(13, 16)],
            ...     use_messiaen_style_ties=True,
            ...     )
            >>> staff = Staff(notes)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'2.
                c'16 \repeatTie
            }

    Set `pitches` to a single pitch or a sequence of pitches.

    Set `durations` to a single duration or a list of durations.

    Returns selection.
    '''
    from abjad.tools import scoretools
    from abjad.tools import selectiontools

    if isinstance(pitches, str):
        pitches = pitches.split()

    if not isinstance(pitches, list):
        pitches = [pitches]

    if isinstance(durations, (numbers.Number, tuple)):
        durations = [durations]

    nonreduced_fractions = [mathtools.NonreducedFraction(_) for _ in durations]
    size = max(len(nonreduced_fractions), len(pitches))
    nonreduced_fractions = sequencetools.repeat_sequence_to_length(
        nonreduced_fractions,
        size,
        )
    pitches = sequencetools.repeat_sequence_to_length(pitches, size)
    Duration = durationtools.Duration
    durations = Duration._group_nonreduced_fractions_by_implied_prolation(
        nonreduced_fractions)

    def _make_unprolated_notes(
        pitches,
        durations,
        decrease_durations_monotonically=decrease_durations_monotonically,
        use_messiaen_style_ties=False,
        ):
        assert len(pitches) == len(durations)
        result = []
        for pitch, duration in zip(pitches, durations):
            result.extend(
                scoretools.make_tied_leaf(
                    scoretools.Note,
                    duration,
                    pitches=pitch,
                    decrease_durations_monotonically=decrease_durations_monotonically,
                    use_messiaen_style_ties=use_messiaen_style_ties,
                    )
                )
        return result

    result = []
    for duration in durations:
        # get factors in denominator of duration group duration not 1 or 2
        factors = set(mathtools.factors(duration[0].denominator))
        factors.discard(1)
        factors.discard(2)
        ps = pitches[0:len(duration)]
        pitches = pitches[len(duration):]
        if len(factors) == 0:
            result.extend(
                _make_unprolated_notes(
                    ps,
                    duration,
                    decrease_durations_monotonically=decrease_durations_monotonically,
                    use_messiaen_style_ties=use_messiaen_style_ties,
                    )
                )
        else:
            # compute prolation
            denominator = duration[0].denominator
            numerator = mathtools.greatest_power_of_two_less_equal(denominator)
            multiplier = (numerator, denominator)
            ratio = 1 / fractions.Fraction(*multiplier)
            duration = [ratio * durationtools.Duration(d) for d in duration]
            ns = _make_unprolated_notes(
                ps,
                duration,
                decrease_durations_monotonically=decrease_durations_monotonically,
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
            t = scoretools.Tuplet(multiplier, ns)
            result.append(t)

    # return result
    result = selectiontools.Selection(result)
    return result
