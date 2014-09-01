# -*- encoding: utf-8 -*-
import numbers
from abjad.tools.abctools.AbjadObject import AbjadObject


class Inversion(AbjadObject):
    r'''Inversion operator.

    ..  container:: example

        ::

            >>> operator_ = pitchtools.Inversion()

        ::

            >>> print(format(operator_))
            pitchtools.Inversion()

    Object model of the twelve-tone inversion operator.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls inversion on `expr`.

        ..  container:: example

            **Example 1.** Inverts numbered pitch-class:

            ::

                >>> operator_ = pitchtools.Inversion() 
                >>> pc = pitchtools.NumberedPitchClass(1)
                >>> operator_(pc)
                NumberedPitchClass(11)

        ..  container:: example

            **Example 2.** Inverts numbered pitch:

            ::

                >>> operator_ = pitchtools.Inversion() 
                >>> pc = pitchtools.NumberedPitch(15)
                >>> operator_(pc)
                NumberedPitch(-15)

        ..  todo:: Implement named pitch-class inversion.

        Returns new object with type equal to that of `expr`.
        '''
        if hasattr(expr, 'invert'):
            result = expr.invert()
        else:
            message = 'do not know how to invert: {!r}.'
            message = message.format(expr)
            raise TypeError(message)
        return result