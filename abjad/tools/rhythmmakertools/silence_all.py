# -*- encoding: utf-8 -*-


def silence_all(use_multimeasure_rests=None):
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

    ..  container:: example

        **Example 3.** Makes rest rhythm-maker with multimeasure rests:

        ::

            >>> mask = rhythmmakertools.silence_all(
            ...     use_multimeasure_rests=True,
            ...     )
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
                            use_multimeasure_rests=True,
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
        use_multimeasure_rests=use_multimeasure_rests,
        )