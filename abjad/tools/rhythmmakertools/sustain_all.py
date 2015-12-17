# -*- coding: utf-8 -*-


def sustain_all():
    r'''Makes sustain mask equal to all ones.

    ..  container:: example

        **Example 1.** Without mask:

            >>> maker = rhythmmakertools.TupletRhythmMaker(
            ...     tuplet_ratios=[(3, 1)],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]

        ::

            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 7/16
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        c'4.
                        c'8
                    }
                }
                {
                    \time 3/8
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'4.
                        c'8
                    }
                }
                {
                    \time 7/16
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        c'4.
                        c'8
                    }
                }
                {
                    \time 3/8
                    \tweak #'text #tuplet-number::calc-fraction-text
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
                indices=(0,),
                period=1,
                )

        ::

            >>> maker = rhythmmakertools.TupletRhythmMaker(
            ...     division_masks=[mask],
            ...     tuplet_ratios=[(3, 1)],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]

        ::

            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
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

    return rhythmmakertools.SustainMask(
        indices=[0],
        period=1,
        )