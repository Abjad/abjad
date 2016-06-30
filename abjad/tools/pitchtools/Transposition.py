# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Transposition(AbjadValueObject):
    r'''Transposition operator.

    ..  container:: example

        **Example.**

        ::

            >>> operator_ = pitchtools.Transposition(2)

        ::

            >>> print(format(operator_))
            pitchtools.Transposition(
                index=2,
                )

    Object model of the twelve-tone tranposition operator.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_index',
        )

    ### INITIALIZER ###

    def __init__(self, index=0):
        self._index = index

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls tranposition on `expr`.

        ..  container:: example

            **Example 1.** Transposes numbered pitch-class up two semitones:

            ::

                >>> operator_ = pitchtools.Transposition(index=2)
                >>> pc = pitchtools.NumberedPitchClass(1)
                >>> operator_(pc)
                NumberedPitchClass(3)

        ..  container:: example

            **Example 2.** Transposes numbered pitch up two semitones:

            ::

                >>> operator_ = pitchtools.Transposition(index=2)
                >>> pitch = pitchtools.NumberedPitch(15)
                >>> operator_(pitch)
                NumberedPitch(17)

        Returns new object with type equal to that of `expr`.
        '''
        if hasattr(expr, 'transpose'):
            result = expr.transpose(self.index)
        else:
            message = 'do not know how to transpose: {!r}.'
            message = message.format(expr)
            raise TypeError(message)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        r'''Gets index of transposition.

        ..  container:: example

            ::

                >>> operator_ = pitchtools.Transposition(index=2)
                >>> operator_.index
                2

        Set to integer, interval or none.
        '''
        return self._index