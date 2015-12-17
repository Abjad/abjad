# -*- coding: utf-8 -*-
from abjad.tools.rhythmmakertools.BooleanPattern import BooleanPattern


class SustainMask(BooleanPattern):
    r'''Sustain mask.

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

    __documentation_section__ = 'Masks'

    __slots__ = (
        )