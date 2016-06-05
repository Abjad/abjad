# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def sustain_every(indices, period, inverted=None):
    r'''Makes sustain mask that matches `indices` at `period`.

    ..  container:: example

        **Example 1.** Sustains every second division:

        ::

            >>> mask = rhythmmakertools.sustain_every(indices=[1], period=2)

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=(1,),
                    period=2,
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_staff(lilypond_file)
            >>> print(format(staff))
            \new RhythmicStaff {
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    c'4.
                }
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    c'4.
                }
            }

    ..  container:: example

        **Example 2.** Sustains every second and third division:

        ::

            >>> mask = rhythmmakertools.sustain_every(indices=[1, 2], period=3)

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=(1, 2),
                    period=3,
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_staff(lilypond_file)
            >>> print(format(staff))
            \new RhythmicStaff {
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    c'4.
                }
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    c'4.
                }
            }

    Returns sustain mask.
    '''
    from abjad.tools import rhythmmakertools
    indices = list(indices)
    pattern = patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        period=period,
        )
    mask = rhythmmakertools.SustainMask(pattern=pattern)
    return mask