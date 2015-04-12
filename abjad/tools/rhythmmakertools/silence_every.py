# -*- encoding: utf-8 -*-


def silence_every(indices, period, use_multimeasure_rests=None):
    r'''Makes silence mask with `indices` set equal to zero at `period`.

    ..  container:: example

        **Example 1.** Silences every second division:

        ::

            >>> mask = rhythmmakertools.silence_every(indices=[1], period=2)

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
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
            >>> f(staff)
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

        **Example 2.** Silences every second and third division:

        ::

            >>> mask = rhythmmakertools.silence_every(indices=[1, 2], period=3)

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
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
            >>> f(staff)
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

    Returns silence mask.
    '''
    from abjad.tools import rhythmmakertools

    indices = list(indices)
    assert isinstance(period, int)
    assert 0 < period

    return rhythmmakertools.SilenceMask(
        indices=indices,
        period=period,
        use_multimeasure_rests=use_multimeasure_rests,
        )