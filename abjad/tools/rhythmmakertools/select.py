# -*- coding: utf-8 -*-


def select(indices=None, invert=None):
    r'''Makes boolean pattern that matches `indices`.

    ..  container:: example

        **Example 1.** Selects index 2:

        ::

            >>> pattern = rhythmmakertools.select([2])

        ::

            >>> print(format(pattern))
            rhythmmakertools.Pattern(
                indices=(2,),
                )

    ..  container:: example

        **Example 2.** Selects indices 2, 3 and 5:

        ::

            >>> pattern = rhythmmakertools.select([2, 3, 5])

        ::

            >>> print(format(pattern))
            rhythmmakertools.Pattern(
                indices=(2, 3, 5),
                )

    Returns boolean pattern.
    '''
    from abjad.tools import rhythmmakertools

    indices = indices or []
    return rhythmmakertools.Pattern(
        indices=indices,
        invert=invert,
        )