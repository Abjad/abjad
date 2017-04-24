# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def silence_last(n=1, inverted=None, use_multimeasure_rests=None):
    r'''Makes silence mask that matches the last `n` indices.

    ..  container:: example

        Silences last division:

        ::

            >>> mask = rhythmmakertools.silence_last()

        ::

            >>> f(mask)
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=[-1],
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
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
                    r4.
                }
            }

    ..  container:: example

        Silences last two divisions:

        ::

            >>> mask = rhythmmakertools.silence_last(n=2)

        ::

            >>> f(mask)
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=[-2, -1],
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
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
                    c'4..
                }
                {
                    \time 3/8
                    c'4.
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

    ..  container:: example

        Silences no last divisions:

        ::

            >>> mask = rhythmmakertools.silence_last(n=0)

        ::

            >>> f(mask)
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=[],
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
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
    indices = list(reversed(range(-1, -n-1, -1)))
    pattern = patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        )
    mask = rhythmmakertools.SilenceMask(
        pattern=pattern,
        use_multimeasure_rests=use_multimeasure_rests,
        )
    return mask
