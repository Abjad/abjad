# -*- coding: utf-8 -*-


def select_last(n=1, inverted=None):
    r'''Makes pattern that matches the last `n` indices.

    ..  container:: example

        **Example 1.** Selects last two divisions for tie creation:

        ::

            >>> pattern = patterntools.select_last(n=2)

        ::

            >>> print(format(pattern))
            patterntools.Pattern(
                indices=(-2, -1),
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

            >>> staff = maker._get_staff(lilypond_file)
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
                    c'4. \repeatTie
                }
            }

        (Tie creation happens between adjacent divisions. Selecting only the
        last division creates no ties.)

    ..  container:: example

        **Example 2.** Selects no divisions for tie creation:

        ::

            >>> pattern = patterntools.select_last(n=0)

        ::

            >>> print(format(pattern))
            patterntools.Pattern(
                indices=(),
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

            >>> staff = maker._get_staff(lilypond_file)
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

    Returns pattern.
    '''
    from abjad.tools import patterntools
    indices = list(reversed(range(-1, -n-1, -1)))
    return patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        )
