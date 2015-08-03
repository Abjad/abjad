# -*- encoding: utf-8 -*-
from abjad.tools.rhythmmakertools.BooleanPattern import BooleanPattern


class SustainMask(BooleanPattern):
    r'''A sustain mask.

    ..  container:: example

        ::

            >>> mask = rhythmmakertools.SustainMask(
            ...     indices=[0, 1, 7],
            ...     period=16,
            ...     )

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                indices=(0, 1, 7),
                period=16,
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output masks'

    __slots__ = ()