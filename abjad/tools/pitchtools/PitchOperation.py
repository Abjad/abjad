# -*- encoding: utf-8 -*-
import collections
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class PitchOperation(AbjadValueObject):
    r'''A pitch operation stack.

    ::

        >>> pitch_operation = pitchtools.PitchOperation(
        ...     operators=(
        ...         pitchtools.Rotation(1),
        ...         pitchtools.Transposition(2),
        ...         ),
        ...     )
        >>> print(format(pitch_operation))
        pitchtools.PitchOperation(
            operators=(
                pitchtools.Rotation(
                    index=1,
                    transpose=True,
                    ),
                pitchtools.Transposition(
                    index=2,
                    ),
                ),
            )

    ::

        >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7])
        >>> pitch_operation(pitch_classes)
        PitchClassSegment([2, 7, 8, 11])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_operators',
        )

    ### INITIALIZER ###

    def __init__(self, operators=None):
        from abjad.tools import pitchtools
        prototype = (
            pitchtools.Inversion,
            pitchtools.Multiplication,
            pitchtools.Transposition,
            pitchtools.Rotation,
            pitchtools.Retrogression,
            )
        if operators is not None:
            if not isinstance(operators, collections.Sequence):
                operators = (operators,)
            assert len(operators)
            assert all(isinstance(_, prototype) for _ in operators)
            operators = tuple(operators)
        self._operators = operators

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls pitch operation on `expr`.

        ::

            >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7])
            >>> pitch_operation(pitch_classes)
            PitchClassSegment([2, 7, 8, 11])

        Returns new pitch expression.
        '''
        if self.operators is None:
            return expr
        for transform in self.operators:
            expr = transform(expr)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def operators(self):
        r'''Gets pitch operators.

        ::

            >>> for operator in pitch_operation.operators:
            ...     print(format(operator))
            ...
            pitchtools.Rotation(
                index=1,
                transpose=True,
                )
            pitchtools.Transposition(
                index=2,
                )

        Returns tuple of operators.
        '''
        return self._operators