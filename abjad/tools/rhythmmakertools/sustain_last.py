# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def sustain_last(n=1, inverted=None):
    r'''Makes sustain mask that matches the last `n` indices.

    ..  container:: example

        Sustains last division:

        ::

            >>> mask = rhythmmakertools.sustain_last()

        ::

            >>> f(mask)
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=[-1],
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

            >>> f(lilypond_file[Staff])
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

        Sustains last two divisions:

        ::

            >>> mask = rhythmmakertools.sustain_last(n=2)

        ::

            >>> f(mask)
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=[-2, -1],
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

            >>> f(lilypond_file[Staff])
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

        Sustains no last divisions:

        ::

            >>> mask = rhythmmakertools.sustain_last(n=0)

        ::

            >>> f(mask)
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=[],
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

            >>> f(lilypond_file[Staff])
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
