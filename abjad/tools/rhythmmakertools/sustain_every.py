# -*- encoding: utf-8 -*-


def sustain_every(indices, period):
    r'''Makes sustain mask with `indices` set equal (at `period`) to sustain.

    ..  container:: example

        **Example 1.** Sustains every second division:

        ::

            >>> mask = rhythmmakertools.sustain_every(indices=[1], period=2)

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                indices=(1,),
                period=2,
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     output_masks=[mask],
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
                indices=(1, 2),
                period=3,
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     output_masks=[mask],
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
    assert isinstance(period, int)
    assert 0 < period

    return rhythmmakertools.SustainMask(
        indices=indices,
        period=period,
        )