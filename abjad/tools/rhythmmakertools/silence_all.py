# -*- encoding: utf-8 -*-


def silence_all():
    r'''Makes silence mask equal to all zeros.

    ..  container:: example

        **Example 1.** Makes mask:

        ::

            >>> mask = rhythmmakertools.silence_all()

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                indices=(0,),
                period=1,
                )

    ..  container:: example

        **Example 2.** Makes rest rhythm-maker:

        ::

            >>> mask = rhythmmakertools.silence_all()
            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     output_masks=[mask],
            ...     )

        ::

            >>> print(format(maker))
            rhythmmakertools.NoteRhythmMaker(
                output_masks=rhythmmakertools.BooleanPatternInventory(
                    (
                        rhythmmakertools.SilenceMask(
                            indices=(0,),
                            period=1,
                            ),
                        )
                    ),
                )

    Returns boolean pattern.
    '''
    from abjad.tools import rhythmmakertools

    return rhythmmakertools.SilenceMask(
        indices=[0],
        period=1,
        )