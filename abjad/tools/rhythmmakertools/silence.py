# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import new


def silence(indices=None, invert=None):
    r'''Makes silence mask that matches `indices`.

    ..  container:: example

        **Example 1.** Silences divisions 1 and 2:

        ::

            >>> mask = rhythmmakertools.silence([1, 2])

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=rhythmmakertools.Pattern(
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
                pattern=rhythmmakertools.Pattern(
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

            >>> pattern_1 = rhythmmakertools.select_all()
            >>> pattern_2 = rhythmmakertools.select_first()
            >>> pattern_3 = rhythmmakertools.select_last()
            >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
            >>> mask = rhythmmakertools.silence(pattern)

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.Pattern(
                            indices=(0,),
                            period=1,
                            ),
                        rhythmmakertools.Pattern(
                            indices=(0,),
                            ),
                        rhythmmakertools.Pattern(
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

        **Example 4.** Works with pattern input and invert flag:

        ::

            >>> pattern_1 = rhythmmakertools.select_all()
            >>> pattern_2 = rhythmmakertools.select_first()
            >>> pattern_3 = rhythmmakertools.select_last()
            >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
            >>> mask = rhythmmakertools.silence(pattern, invert=True)

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                pattern=rhythmmakertools.CompoundPattern(
                    (
                        rhythmmakertools.Pattern(
                            indices=(0,),
                            period=1,
                            ),
                        rhythmmakertools.Pattern(
                            indices=(0,),
                            ),
                        rhythmmakertools.Pattern(
                            indices=(-1,),
                            ),
                        ),
                    invert=True,
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
    prototype = (rhythmmakertools.Pattern, rhythmmakertools.CompoundPattern)
    if isinstance(indices, prototype):
        pattern = indices
    else:
        pattern = rhythmmakertools.Pattern(
            indices=indices,
            invert=invert,
            )
    pattern = new(pattern, invert=invert)
    return rhythmmakertools.SilenceMask(pattern=pattern)