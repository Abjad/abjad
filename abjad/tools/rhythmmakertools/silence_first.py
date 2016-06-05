# -*- coding: utf-8 -*-
from abjad.tools import patterntools


def silence_first(n=1, inverted=None, use_multimeasure_rests=None):
    r'''Makes silence mask that matches the first `n` indices.

    ..  container:: example

        **Example 1.** Silences first division:

        ::

            >>> mask = rhythmmakertools.silence_first()

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=(0,),
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

            >>> staff = rhythm_maker._get_staff(lilypond_file)
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
                pattern=patterntools.Pattern(
                    indices=(0, 1),
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

        **Example 3.** Silences no first divisions:

        ::

            >>> mask = rhythmmakertools.silence_first(n=0)

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=(),
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

            >>> staff = rhythm_maker._get_staff(lilypond_file)
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
    indices = list(range(n))
    pattern = patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        )
    mask = rhythmmakertools.SilenceMask(
        pattern=pattern,
        use_multimeasure_rests=use_multimeasure_rests,
        )
    return mask