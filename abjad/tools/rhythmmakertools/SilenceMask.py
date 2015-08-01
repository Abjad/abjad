# -*- encoding: utf-8 -*-
from abjad.tools.rhythmmakertools.BooleanPattern import BooleanPattern


class SilenceMask(BooleanPattern):
    r'''A silence mask.

    ..  container:: example

        ::

            >>> mask = rhythmmakertools.SilenceMask(
            ...     indices=[0, 1, 7],
            ...     period=16,
            ...     )

        ::

            >>> print(format(mask))
            rhythmmakertools.SilenceMask(
                indices=(0, 1, 7),
                period=16,
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output masks'

    __slots__ = (
        '_use_multimeasure_rests',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        indices=None,
        period=None,
        invert=None,
        use_multimeasure_rests=None,
        ):
        superclass = super(SilenceMask, self)
        superclass.__init__(
            indices=indices,
            period=period,
            invert=None,
            )
        if use_multimeasure_rests is not None:
            assert isinstance(use_multimeasure_rests, type(True))
        self._use_multimeasure_rests = use_multimeasure_rests

    ### PUBLIC PROPERTIES ###

    @property
    def use_multimeasure_rests(self):
        r'''Is true when silence mask should use multimeasure rests.

        ..  container:: example

            **Example 1.** Without multimeasure rests:

            ::

                >>> mask = rhythmmakertools.SilenceMask(
                ...     indices=[0, 1, 7],
                ...     period=16,
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
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     use_multimeasure_rests=True,
                ...     )

            ::

                >>> mask.use_multimeasure_rests
                True

        Set to true, false or none.
        '''
        return self._use_multimeasure_rests