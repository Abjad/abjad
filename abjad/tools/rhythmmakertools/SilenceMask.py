# -*- coding: utf-8 -*-
from abjad.tools import patterntools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SilenceMask(AbjadValueObject):
    r'''Silence mask.

    ..  container:: example

        ::

            >>> pattern = patterntools.select_every([0, 1, 7], period=16)
            >>> mask = rhythmmakertools.SilenceMask(pattern)

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
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
        '_use_multimeasure_rests',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        use_multimeasure_rests=None,
        ):
        from abjad.tools import rhythmmakertools
        prototype = (
            patterntools.Pattern,
            patterntools.CompoundPattern,
            )
        if pattern is None:
            pattern = patterntools.select_all()
        assert isinstance(pattern, prototype), repr(pattern)
        self._pattern = pattern
        if use_multimeasure_rests is not None:
            assert isinstance(use_multimeasure_rests, type(True))
        self._use_multimeasure_rests = use_multimeasure_rests

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        Returns pattern.
        '''
        return self._pattern

    @property
    def use_multimeasure_rests(self):
        r'''Is true when silence mask should use multimeasure rests.

        ..  container:: example

            **Example 1.** Without multimeasure rests:

            ::

            
                >>> mask = rhythmmakertools.SilenceMask(
                ...     patterntools.select_every([0, 1, 7], period=16),
                ...     use_multimeasure_rests=False,
                ...     )

            ::

                >>> mask.use_multimeasure_rests
                False

            This is default behavior.

        ..  container:: example

            **Example 2.** With multimeasure rests:

            ::

                >>> mask = rhythmmakertools.SilenceMask(
                ...     patterntools.select_every([0, 1, 7], period=16),
                ...     use_multimeasure_rests=True,
                ...     )

            ::

                >>> mask.use_multimeasure_rests
                True

        Set to true, false or none.
        '''
        return self._use_multimeasure_rests