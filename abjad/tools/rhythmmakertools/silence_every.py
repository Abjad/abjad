# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def silence_every(
    indices, 
    period=None, 
    inverted=None, 
    use_multimeasure_rests=None,
    ):
    r'''Makes silence mask that matches `indices` at `period`.

    ..  container:: example

        Silences every second division:

        ::

            >>> mask = rhythmmakertools.silence_every(indices=[1], period=2)

        ::

            >>> f(mask)
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=[1],
                    period=2,
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

        Silences every second and third division:

        ::

            >>> mask = rhythmmakertools.silence_every(indices=[1, 2], period=3)

        ::

            >>> f(mask)
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=[1, 2],
                    period=3,
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

        Silences every division except the last:

        ::

            >>> mask = rhythmmakertools.silence_every(indices=[-1], inverted=True)

        ::

            >>> f(mask)
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=[-1],
                    inverted=True,
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

    Returns silence mask.
    '''
    from abjad.tools import rhythmmakertools
    pattern = patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        period=period,
        )
    mask = rhythmmakertools.SilenceMask(
        pattern=pattern,
        use_multimeasure_rests=use_multimeasure_rests,
        )
    return mask
