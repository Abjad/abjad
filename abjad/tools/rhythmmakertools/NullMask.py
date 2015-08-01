# -*- encoding: utf-8 -*-
from abjad.tools.rhythmmakertools.BooleanPattern import BooleanPattern


class NullMask(BooleanPattern):
    r'''A sustain mask.

    ..  container:: example

        ::

            >>> mask = rhythmmakertools.NullMask(
            ...     indices=[0, 1, 7],
            ...     period=16,
            ...     )

        ::

            >>> print(format(mask))
            rhythmmakertools.NullMask(
                indices=(0, 1, 7),
                period=16,
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output masks'

    __slots__ = ()