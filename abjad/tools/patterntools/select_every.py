# -*- coding: utf-8 -*-


def select_every(indices, period=None, inverted=None):
    r'''Makes pattern that matches `indices` at `period`.

    ..  container:: example

        **Example 1.** Selects every second division:

        ::

            >>> mask = patterntools.select_every(indices=[1], period=2)

        ::

            >>> print(format(mask))
            patterntools.Pattern(
                indices=(1,),
                period=2,
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_staff(lilypond_file)
            >>> print(format(staff))
            \new RhythmicStaff {
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    r4.
                }
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    r4.
                }
            }

    ..  container:: example

        **Example 2.** Selects every second and third division:

        ::

            >>> mask = patterntools.select_every(indices=[1, 2], period=3)

        ::

            >>> print(format(mask))
            patterntools.Pattern(
                indices=(1, 2),
                period=3,
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_staff(lilypond_file)
            >>> print(format(staff))
            \new RhythmicStaff {
                {
                    \time 7/16
                    c'4..
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
                    c'4.
                }
            }


    Returns pattern.
    '''
    from abjad.tools import patterntools
    return patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        period=period,
        )
