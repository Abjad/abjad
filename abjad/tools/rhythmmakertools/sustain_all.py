# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def sustain_all(inverted=None):
    r'''Makes sustain mask that matches all indices.

    ..  container:: example

        **Example 1.** Without mask:

            >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
            ...     tuplet_ratios=[(3, 1)],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]

        ::

            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        c'4.
                        c'8
                    }
                }
                {
                    \time 3/8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'4.
                        c'8
                    }
                }
                {
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        c'4.
                        c'8
                    }
                }
                {
                    \time 3/8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'4.
                        c'8
                    }
                }
            }

    ..  container:: example

        **Example 2.** With mask:

        ::

            >>> mask = rhythmmakertools.sustain_all()

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=(0,),
                    period=1,
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.TupletRhythmMaker(
            ...     division_masks=[mask],
            ...     tuplet_ratios=[(3, 1)],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]

        ::

            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_staff(lilypond_file)
            >>> f(staff)
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
    pattern = patterntools.Pattern(
        indices=[0],
        inverted=inverted,
        period=1,
        )
    mask = rhythmmakertools.SustainMask(pattern=pattern)
    return mask