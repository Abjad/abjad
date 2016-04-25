# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Multiplication(AbjadValueObject):
    r'''Multiplication operator.

    ..  container:: example

        **Example 1.**

        ::

            >>> operator_ = pitchtools.Multiplication(index=5)

        ::

            >>> print(format(operator_))
            pitchtools.Multiplication(
                index=5,
                )

    Object model of the twelve-tone multiplication operator.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_index',
        )

    ### INITIALIZER ###

    def __init__(self, index=5):
        self._index = index

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls tranposition on `expr`.

        ..  container:: example

            **Example 1.** Multiplies numbered pitch-class by ``5``:

            ::

                >>> operator_ = pitchtools.Multiplication(index=5)
                >>> pc = pitchtools.NumberedPitchClass(4)
                >>> operator_(pc)
                NumberedPitchClass(8)

        ..  container:: example

            **Example 2.** Multiplies numbered pitch-pitch by ``7``:

            ::

                >>> operator_ = pitchtools.Multiplication(index=7)
                >>> pitch = pitchtools.NumberedPitchClass(4)
                >>> operator_(pitch)
                NumberedPitchClass(4)

        Returns new object with type equal to that of `expr`.
        '''
        if hasattr(expr, 'multiply'):
            result = expr.multiply(self.index)
        else:
            message = 'do not know how to multiply: {!r}.'
            message = message.format(expr)
            raise TypeError(message)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        r'''Gets index of multiplication.

        ..  container:: example

            ::

                >>> operator_ = pitchtools.Multiplication(index=5)
                >>> operator_.index
                5

        Set to integer or none.
        '''
        return self._index
