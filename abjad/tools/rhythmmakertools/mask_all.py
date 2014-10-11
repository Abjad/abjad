# -*- encoding: utf-8 -*-


def mask_all():
    r'''Makes boolean pattern equal to all zeros.

    ..  container:: example

        **Example 1.** Makes mask:

        ::

            >>> mask = rhythmmakertools.mask_all()

        ::

            >>> print(format(mask))
            rhythmmakertools.BooleanPattern(
                indices=(0,),
                period=1,
                )

    ..  container:: example

        **Example 2.** Makes rest rhythm-maker:

        ::

            >>> mask = rhythmmakertools.mask_all()
            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     output_masks=[mask],
            ...     )

        ::

            >>> print(format(maker))
            rhythmmakertools.NoteRhythmMaker(
                output_masks=(
                    rhythmmakertools.BooleanPattern(
                        indices=(0,),
                        period=1,
                        ),
                    ),
                )

    Returns boolean pattern.
    '''
    from abjad.tools import rhythmmakertools

    return rhythmmakertools.BooleanPattern(
        indices=[0],
        period=1,
        )