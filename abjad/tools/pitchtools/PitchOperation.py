# -*- coding: utf-8 -*-
import collections
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class PitchOperation(AbjadValueObject):
    r'''Pitch operation.

    ..  container:: example

        **Example 1.** Rotation followed by transposition:

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
            sequencetools.Duplication,
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

    ### PRIVATE METHODS ###

    def _with_operator(self, operator):
        operators = self.operators or ()
        operators = operators + (operator,)
        return type(self)(operators)

    ### PUBLIC METHODS ###

    def duplicate(self, counts=None, indices=None, period=None):
        r'''Configures pitch operation to duplicate pitches by `counts`, with
        optional `indices` and `period`.

        ..  container:: example

            ::

                >>> pitch_operation = pitchtools.PitchOperation()
                >>> pitch_operation = pitch_operation.duplicate(1)
                >>> print(format(pitch_operation))
                pitchtools.PitchOperation(
                    operators=(
                        sequencetools.Duplication(
                            counts=1,
                            ),
                        ),
                    )

        Returns new pitch operation.
        '''
        operator = sequencetools.Duplication(
            counts=counts,
            indices=indices,
            period=period,
            )
        return self._with_operator(operator)

    def invert(self, axis=None):
        r'''Configures pitch operation to invert pitches by `index`.

        ..  container:: example

            ::

                >>> pitch_operation = pitchtools.PitchOperation()
                >>> pitch_operation = pitch_operation.invert(2)
                >>> print(format(pitch_operation))
                pitchtools.PitchOperation(
                    operators=(
                        pitchtools.Inversion(
                            axis=pitchtools.NamedPitch("d'"),
                            ),
                        ),
                    )

        Returns new pitch operation.
        '''
        from abjad.tools import pitchtools
        operator = pitchtools.Inversion(axis=axis)
        return self._with_operator(operator)

    def multiply(self, index=1):
        r'''Configures pitch operation to multiply pitch-classes by `index`.

        ..  container:: example

            ::

                >>> pitch_operation = pitchtools.PitchOperation()
                >>> pitch_operation = pitch_operation.multiply(3)
                >>> print(format(pitch_operation))
                pitchtools.PitchOperation(
                    operators=(
                        pitchtools.Multiplication(
                            index=3,
                            ),
                        ),
                    )

        Returns new pitch operation.
        '''
        from abjad.tools import pitchtools
        operator = pitchtools.Multiplication(index=index)
        return self._with_operator(operator)

    def retrograde(self, period=None):
        r'''Configures pitch operation to retrograde pitches.

        ..  container:: example

            ::

                >>> pitch_operation = pitchtools.PitchOperation()
                >>> pitch_operation = pitch_operation.retrograde()
                >>> print(format(pitch_operation))
                pitchtools.PitchOperation(
                    operators=(
                        pitchtools.Retrogression(),
                        ),
                    )

        Returns new pitch operation.
        '''
        from abjad.tools import pitchtools
        operator = pitchtools.Retrogression(period=period)
        return self._with_operator(operator)

    def rotate(self, index=0, transpose=True, period=None):
        r'''Configures pitch operation to rotate pitches by `index`.

        ..  container:: example

            ::

                >>> pitch_operation = pitchtools.PitchOperation()
                >>> pitch_operation = pitch_operation.rotate(-1)
                >>> print(format(pitch_operation))
                pitchtools.PitchOperation(
                    operators=(
                        pitchtools.Rotation(
                            index=-1,
                            transpose=True,
                            ),
                        ),
                    )

        Returns new pitch operation.
        '''
        from abjad.tools import pitchtools
        operator = pitchtools.Rotation(
            index=index,
            transpose=transpose,
            period=period,
            )
        return self._with_operator(operator)

    def transpose(self, index=0):
        r'''Configures pitch operation to transpose pitches by `index`.

        ..  container:: example

            ::

                >>> pitch_operation = pitchtools.PitchOperation()
                >>> pitch_operation = pitch_operation.transpose(1)
                >>> print(format(pitch_operation))
                pitchtools.PitchOperation(
                    operators=(
                        pitchtools.Transposition(
                            index=1,
                            ),
                        ),
                    )

        Returns new pitch operation.
        '''
        from abjad.tools import pitchtools
        operator = pitchtools.Transposition(index=index)
        return self._with_operator(operator)

    ### PUBLIC PROPERTIES ###

    @property
    def operators(self):
        r'''Gets pitch operators.

        ::

            >>> pitch_operation = pitchtools.PitchOperation()
            >>> pitch_operation = pitch_operation.rotate(1)
            >>> pitch_operation = pitch_operation.transpose(2)
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
