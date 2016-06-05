# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def sustain_last(n=1, inverted=None):
    r'''Makes sustain mask that matches the last `n` indices.

    ..  container:: example

        **Example 1.** Sustains last division:

        ::

            >>> mask = rhythmmakertools.sustain_last()

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=(-1,),
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         rhythmmakertools.silence_all(),
            ...         mask,
            ...         ],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_staff(lilypond_file)
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
                pattern=patterntools.Pattern(
                    indices=(-2, -1),
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         rhythmmakertools.silence_all(),
            ...         mask
            ...         ],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_staff(lilypond_file)
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
                pattern=patterntools.Pattern(
                    indices=(),
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         rhythmmakertools.silence_all(),
            ...         mask,
            ...         ],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_staff(lilypond_file)
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

    indices = list(reversed(range(-1, -n-1, -1)))
    pattern = patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        )
    mask = rhythmmakertools.SustainMask(pattern=pattern)
    return mask