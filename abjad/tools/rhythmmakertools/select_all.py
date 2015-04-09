# -*- encoding: utf-8 -*-


def select_all():
    r'''Makes cyclic boolean pattern equal to all indices.

    ..  container:: example

        **Example 1.** Selects all divisions for tie creation:

        ::

            >>> pattern = rhythmmakertools.select_all()

        ::

            >>> print(format(pattern))
            rhythmmakertools.BooleanPattern(
                indices=(0,),
                period=1,
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     tie_specifier=rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=pattern,
            ...         use_messiaen_style_ties=True,
            ...         ),
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
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
                    c'4. \repeatTie
                }
                {
                    \time 7/16
                    c'4.. \repeatTie
                }
                {
                    \time 3/8
                    c'4. \repeatTie
                }
            }

    Returns boolean pattern.
    '''
    from abjad.tools import rhythmmakertools

    return rhythmmakertools.BooleanPattern(
        indices=[0],
        period=1,
        )