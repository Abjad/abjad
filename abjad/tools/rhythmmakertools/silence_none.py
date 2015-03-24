# -*- encoding: utf-8 -*-


def silence_none():
    r'''Makes silence mask equal to all ones.

    ..  container:: example

        **Example 1.** Makes mask:

        ::

            >>> mask = rhythmmakertools.silence_none()

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                indices=(),
                period=1,
                )

    ..  container:: example

        **Example 2.** Makes note rhythm-maker. Effectively applies no mask:

        ::

            >>> mask = rhythmmakertools.silence_none()
            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     output_masks=[mask],
            ...     )

        ::

            >>> print(format(maker))
            rhythmmakertools.NoteRhythmMaker(
                output_masks=rhythmmakertools.BooleanPatternInventory(
                    (
                        rhythmmakertools.SilenceMask(
                            indices=(),
                            period=1,
                            ),
                        )
                    ),
                )

    Returns boolean pattern.
    '''
    from abjad.tools import rhythmmakertools

    return rhythmmakertools.SilenceMask(
        indices=[],
        period=1,
        )