# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools.topleveltools import attach


def make_leaves_from_talea(
    talea,
    talea_denominator,
    decrease_durations_monotonically=True,
    forbidden_written_duration=None,
    spell_metrically=None,
    use_messiaen_style_ties=False,
    ):
    r'''Makes leaves from `talea`.

    Interprets positive elements in `talea` as notes numerators.

    Interprets negative elements in `talea` as rests numerators.

    Sets the pitch of all notes to middle C.

    ..  container:: example

        **Example 1.** Makes leaves from talea:

        ::

            >>> leaves = scoretools.make_leaves_from_talea([3, -3, 5, -5], 16)
            >>> staff = Staff(leaves)
            >>> staff.context_name = 'RhythmicStaff'
            >>> time_signature = TimeSignature((4, 4))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new RhythmicStaff {
                \time 4/4
                c'8.
                r8.
                c'4 ~
                c'16
                r4
                r16
            }

    ..  container:: example

        **Example 2.** Increases durations monotonically:

        ::

            >>> leaves = scoretools.make_leaves_from_talea(
            ...     [3, -3, 5, -5], 16,
            ...     decrease_durations_monotonically=False,
            ...     )
            >>> staff = Staff(leaves)
            >>> staff.context_name = 'RhythmicStaff'
            >>> time_signature = TimeSignature((4, 4))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new RhythmicStaff {
                \time 4/4
                c'8.
                r8.
                c'16 ~
                c'4
                r16
                r4
            }

    ..  container:: example

        **Example 3.** Forbids written durations greater than or equal
        to a half note:

        ::

            >>> leaves = scoretools.make_leaves_from_talea(
            ...     [3, -3, 5, -5], 16,
            ...     forbidden_written_duration=Duration(1, 4),
            ...     )
            >>> staff = Staff(leaves)
            >>> staff.context_name = 'RhythmicStaff'
            >>> time_signature = TimeSignature((4, 4))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new RhythmicStaff {
                \time 4/4
                c'8.
                r8.
                c'8 ~
                c'8 ~
                c'16
                r8
                r8
                r16
            }

    ..  container:: example

        **Example 4.** Spells unassignable durations metrically:

        ::

            >>> leaves = scoretools.make_leaves_from_talea(
            ...     [3, -3, 5, -5], 16,
            ...     spell_metrically='unassignable',
            ...     )
            >>> staff = Staff(leaves)
            >>> staff.context_name = 'RhythmicStaff'
            >>> time_signature = TimeSignature((4, 4))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new RhythmicStaff {
                \time 4/4
                c'8.
                r8.
                c'8. ~
                c'8
                r8.
                r8
            }

    ..  container:: example

        **Example 5.** Uses Messiaen-style ties:

        ::

            >>> leaves = scoretools.make_leaves_from_talea(
            ...     [5, 9], 8,
            ...     spell_metrically='unassignable',
            ...     use_messiaen_style_ties=True,
            ...     )
            >>> staff = Staff(leaves)
            >>> staff.context_name = 'RhythmicStaff'
            >>> time_signature = TimeSignature((4, 4))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new RhythmicStaff {
                \time 4/4
                c'4.
                c'4 \repeatTie
                c'4.
                c'4. \repeatTie
                c'4. \repeatTie
            }

    Returns selection.
    '''
    from abjad.tools import metertools
    from abjad.tools import scoretools
    from abjad.tools import spannertools

    assert all(x != 0 for x in talea), repr(talea)

    result = []
    for note_value in talea:
        if 0 < note_value:
            pitches = [0]
        else:
            pitches = [None]
        division = durationtools.Duration(
            abs(note_value),
            talea_denominator,
            )
        if (spell_metrically is True or
            (spell_metrically == 'unassignable' and
            not mathtools.is_assignable_integer(division.numerator))):
            meter = metertools.Meter(division)
            rhythm_tree_container = meter.root_node
            durations = [_.duration for _ in rhythm_tree_container]
        else:
            durations = [division]
        leaves = scoretools.make_leaves(
            pitches,
            durations,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
        if (
            1 < len(leaves) and
            not leaves[0]._has_spanner(spannertools.Tie) and
            not isinstance(leaves[0], scoretools.Rest)
            ):
            tie = spannertools.Tie(
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
            attach(tie, leaves[:])
        result.extend(leaves)
    result = selectiontools.Selection(result)
    return result
