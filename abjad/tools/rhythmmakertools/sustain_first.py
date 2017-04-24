# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def sustain_first(n=1, inverted=None):
    r'''Makes sustain mask that matches the first `n` indices.

    ..  container:: example

        Sustains first division:

        ::

            >>> mask = rhythmmakertools.sustain_first()

        ::

            >>> f(mask)
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=[0],
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
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
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
                {
                    \time 7/16
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
                {
                    \time 3/8
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
            }

    ..  container:: example

        Sustains first two divisions:

        ::

            >>> mask = rhythmmakertools.sustain_first(n=2)

        ::

            >>> f(mask)
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=[0, 1],
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
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
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
                {
                    \time 3/8
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
            }

    Returns sustain mask.
    '''
    from abjad.tools import rhythmmakertools
    indices = list(range(n))
    pattern = patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        )
    mask = rhythmmakertools.SustainMask(pattern=pattern)
    return mask
