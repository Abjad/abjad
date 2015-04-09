# -*- encoding: utf-8 -*-


def silence_first(n=1, use_multimeasure_rests=None):
    r'''Makes silence mask with first `n` indices equal to zero.

    ..  container:: example

        **Example 1.** Silences first division:

        ::

            >>> mask = rhythmmakertools.silence_first()

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                indices=(0,),
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
                    c'4.
                }
            }

    ..  container:: example

        **Example 2.** Silences first two divisions:

        ::

            >>> mask = rhythmmakertools.silence_first(n=2)

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                indices=(0, 1),
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

    ..  container:: example

        **Example 3.** Silences no first divisions:

        ::

            >>> mask = rhythmmakertools.silence_first(n=0)

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                indices=(),
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

    Returns silence mask.
    '''
    from abjad.tools import rhythmmakertools

    assert 0 <= n, repr(n)
    indices = list(range(n))

    return rhythmmakertools.SilenceMask(
        indices=indices,
        use_multimeasure_rests=use_multimeasure_rests,
        )