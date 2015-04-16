# -*- encoding: utf-8 -*-


def sustain_last(n=1):
    r'''Makes sustain mask with last `n` indices set.

    ..  container:: example

        **Example 1.** Sustains last division:

        ::

            >>> mask = rhythmmakertools.sustain_last()

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                indices=(-1,),
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     output_masks=[
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
                    c'4.
                }
            }

    ..  container:: example

        **Example 2.** Sustains last two divisions:

        ::

            >>> mask = rhythmmakertools.sustain_last(n=2)

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                indices=(-2, -1),
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     output_masks=[
            ...         rhythmmakertools.silence_all(),
            ...         mask
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

        **Example 3.** Sustains no last divisions:

        ::

            >>> mask = rhythmmakertools.sustain_last(n=0)

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                indices=(),
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     output_masks=[
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

    Returns sustain mask.
    '''
    from abjad.tools import rhythmmakertools

    assert 0 <= n, repr(n)
    indices = list(reversed(range(-1, -n-1, -1)))

    return rhythmmakertools.SustainMask(
        indices=indices,
        )