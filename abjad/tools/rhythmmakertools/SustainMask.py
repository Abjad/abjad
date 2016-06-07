# -*- coding: utf-8 -*-
from abjad.tools import patterntools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SustainMask(AbjadValueObject):
    r'''Sustain mask.

    ..  container:: example

        ::

            >>> mask = rhythmmakertools.SustainMask(
            ...     pattern=patterntools.select_every([0, 1, 7], period=16),
            ...     )

        ::

            >>> print(format(mask))
            rhythmmakertools.SustainMask(
                pattern=patterntools.Pattern(
                    indices=(0, 1, 7),
                    period=16,
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Masks'

    __slots__ = (
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        ):
        prototype = (
            patterntools.Pattern,
            patterntools.CompoundPattern,
            )
        if pattern is None:
            pattern = patterntools.select_all()
        assert isinstance(pattern, prototype), repr(pattern)
        self._pattern = pattern

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        Returns pattern.
        '''
        return self._pattern