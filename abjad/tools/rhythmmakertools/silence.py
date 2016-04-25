# -*- coding: utf-8 -*-
from abjad.tools import patterntools
from abjad.tools.topleveltools import new


def silence(indices=None, inverted=None):
    r'''Makes silence mask that matches `indices`.

    ..  container:: example

        **Example 1.** Silences divisions 1 and 2:

        ::

            >>> mask = rhythmmakertools.silence([1, 2])

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=(1, 2),
                    ),
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
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
            >>> print(format(staff))
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

        **Example 2.** Silences divisions -1 and -2:

        ::

            >>> mask = rhythmmakertools.silence([-1, -2])

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=patterntools.Pattern(
                    indices=(-1, -2),
                    ),
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
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
            >>> print(format(staff))
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

        **Example 3.** Works with pattern input:

        ::

            >>> pattern_1 = patterntools.select_all()
            >>> pattern_2 = patterntools.select_first()
            >>> pattern_3 = patterntools.select_last()
            >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
            >>> mask = rhythmmakertools.silence(pattern)

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
                    operator='xor',
                    ),
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
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
            >>> print(format(staff))
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

        **Example 4.** Works with pattern input and inverted flag:

        ::

            >>> pattern_1 = patterntools.select_all()
            >>> pattern_2 = patterntools.select_first()
            >>> pattern_3 = patterntools.select_last()
            >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
            >>> mask = rhythmmakertools.silence(pattern, inverted=True)

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

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
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
            inverted=inverted,
            )
    pattern = new(pattern, inverted=inverted)
    return rhythmmakertools.SilenceMask(pattern=pattern)
