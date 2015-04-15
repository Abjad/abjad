# -*- encoding: utf-8 -*-


def select(indices=[]):
    r'''Makes acyclic boolean pattern equal to `indices`.

    ..  container:: example

        **Example 1.** Selects index 2:

        ::

            >>> pattern = rhythmmakertools.select([2])

        ::

            >>> print(format(pattern))
            rhythmmakertools.BooleanPattern(
                indices=(2,),
                )

    ..  container:: example

        **Example 2.** Selects indices 2, 3 and 5:

        ::

            >>> pattern = rhythmmakertools.select([2, 3, 5])

        ::

            >>> print(format(pattern))
            rhythmmakertools.BooleanPattern(
                indices=(2, 3, 5),
                )

    Returns boolean pattern.
    '''
    from abjad.tools import rhythmmakertools

    assert all(isinstance(_, int) for _ in indices), repr(indices)

    return rhythmmakertools.BooleanPattern(
        indices=indices,
        )