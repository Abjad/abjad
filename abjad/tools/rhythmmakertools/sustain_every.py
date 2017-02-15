# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def sustain_every(indices, period, inverted=None):
    r'''Makes sustain mask that matches `indices` at `period`.

    ..  container:: example

        Sustains every second division:

        ::

            >>> mask = rhythmmakertools.sustain_every(indices=[1], period=2)

        ::

            >>> f(mask)
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=[1],
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

            >>> f(lilypond_file[Staff])
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

        Sustains every second and third division:

        ::

            >>> mask = rhythmmakertools.sustain_every(indices=[1, 2], period=3)

        ::

            >>> f(mask)
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=[1, 2],
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

            >>> f(lilypond_file[Staff])
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
