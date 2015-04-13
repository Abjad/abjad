# -*- encoding: utf-8 -*-


def sustain_first(n=1):
    r'''Makes sustain mask equal to first `n` indices.

    ..  container:: example

        **Example 1.** Sustains first division:

        ::

            >>> mask = rhythmmakertools.sustain_first()

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                indices=(0,),
                )

        ::

            >>> maker = rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
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
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
                {
                    \time 7/16
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
                {
                    \time 3/8
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
            }

    ..  container:: example

        **Example 2.** Sustains first two divisions:

        ::

            >>> mask = rhythmmakertools.sustain_first(n=2)

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                indices=(0, 1),
                )

        ::

            >>> maker = rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
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
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
                {
                    \time 3/8
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
            }

    Returns sustain mask.
    '''
    from abjad.tools import rhythmmakertools

    assert 0 <= n, repr(n)
    indices = list(range(n))

    return rhythmmakertools.SustainMask(
        indices=indices,
        )