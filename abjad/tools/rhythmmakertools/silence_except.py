# -*- coding: utf-8 -*-
from abjad.tools import patterntools
from abjad.tools.topleveltools import new


def silence_except(indices=None):
    r'''Makes silence mask that matches all indices except `indices`.

    ..  container:: example

        **Example 1.** Silences divisions except 1 and 2:

        ::

            >>> mask = rhythmmakertools.silence_except([1, 2])

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=(1, 2),
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

            >>> staff = rhythm_maker._get_staff(lilypond_file)
            >>> print(format(staff))
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
                    r4.
                }
            }

    ..  container:: example

        **Example 2.** Silences divisions except -1 and -2:

        ::

            >>> mask = rhythmmakertools.silence_except([-1, -2])

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=(-1, -2),
                    inverted=True,
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
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
            >>> print(format(staff))
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

        **Example 3.** Works with pattern input:

        ::

            >>> pattern_1 = patterntools.select_all()
            >>> pattern_2 = patterntools.select_first()
            >>> pattern_3 = patterntools.select_last()
            >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
            >>> mask = rhythmmakertools.silence_except(pattern)

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0,),
                            period=1,
                            ),
                        patterntools.Pattern(
                            indices=(0,),
                            ),
                        patterntools.Pattern(
                            indices=(-1,),
                            ),
                        ),
                    inverted=True,
                    operator='xor',
                    ),
                )

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
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
            >>> print(format(staff))
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
                    r4.
                }
            }

    Equivalent to ``silence(..., inverted=True)``.

    Returns silence mask.
    '''
    from abjad.tools import rhythmmakertools
    indices = indices or []
    prototype = (patterntools.Pattern, patterntools.CompoundPattern)
    if isinstance(indices, prototype):
        pattern = indices
    else:
        pattern = patterntools.Pattern(
            indices=indices,
            )
    pattern = new(pattern, inverted=True)
    return rhythmmakertools.SilenceMask(pattern=pattern)