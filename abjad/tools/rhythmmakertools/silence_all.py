# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def silence_all(inverted=None, use_multimeasure_rests=None):
    r'''Makes silence that matches all indices.

    ..  container:: example

        **Example 1.** Silences all divisions:

        ::

            >>> mask = rhythmmakertools.silence_all()

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=(0,),
                    period=1,
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
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 7/16
                    r4..
                }
                {
                    \time 3/8
                    r4.
                }
                {
                    \time 7/16
                    r4..
                }
                {
                    \time 3/8
                    r4.
                }
            }

    ..  container:: example

        **Example 2.** Silences all divisions with multimeasure rests:

        ::

            >>> mask = rhythmmakertools.silence_all(
            ...     use_multimeasure_rests=True,
            ...     )
            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )

        ::

            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
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
                    R1 * 7/16
                }
                {
                    \time 3/8
                    R1 * 3/8
                }
                {
                    \time 7/16
                    R1 * 7/16
                }
                {
                    \time 3/8
                    R1 * 3/8
                }
            }

    Returns silence mask.
    '''
    from abjad.tools import rhythmmakertools
    pattern = patterntools.Pattern(
        indices=[0],
        inverted=inverted,
        period=1,
        )
    mask = rhythmmakertools.SilenceMask(
        pattern=pattern,
        use_multimeasure_rests=use_multimeasure_rests,
        )
    return mask