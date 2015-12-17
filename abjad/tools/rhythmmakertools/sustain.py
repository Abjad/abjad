# -*- coding: utf-8 -*-


def sustain(indices, invert=None):
    r'''Makes sustain mask that matches `indices`.

    ..  container:: example

        **Example 1.** Sustains divisions 1 and 2:

        ::

            >>> mask = rhythmmakertools.sustain([1, 2])

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                indices=(1, 2),
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         rhythmmakertools.silence_all(),
            ...         mask,
            ...         ],
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
            >>> print(format(staff))
            \new RhythmicStaff {
                {
                    \time 7/16
                    r4..
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
                    r4.
                }
            }

    ..  container:: example

        **Example 2.** Sustains divisions -1 and -2:

        ::

            >>> mask = rhythmmakertools.sustain([-1, -2])

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                indices=(-1, -2),
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         rhythmmakertools.silence_all(),
            ...         mask,
            ...         ],
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
            >>> print(format(staff))
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
    return rhythmmakertools.SustainMask(
        indices=indices,
        invert=invert,
        )