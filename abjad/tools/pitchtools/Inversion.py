# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Inversion(AbjadValueObject):
    r'''Inversion operator.

    ..  container:: example

        **Example 1.**

        ::

            >>> operator_ = pitchtools.Inversion()

        ::

            >>> print(format(operator_))
            pitchtools.Inversion()

    Object model of the twelve-tone inversion operator.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_axis',
        )

    ### INITIALIZER ###

    def __init__(self, axis=None):
        from abjad.tools import pitchtools
        if axis is not None:
            axis = pitchtools.NamedPitch(axis)
        self._axis = axis

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls inversion on `expr`.

        ..  container:: example

            **Example 1.** Inverts numbered pitch-class:

            ::

                >>> operator_ = pitchtools.Inversion()
                >>> expr = pitchtools.NumberedPitchClass(1)
                >>> operator_(expr)
                NumberedPitchClass(11)

        ..  container:: example

            **Example 2.** Inverts numbered pitch:

            ::

                >>> operator_ = pitchtools.Inversion()
                >>> expr = pitchtools.NumberedPitch(15)
                >>> operator_(expr)
                NumberedPitch(-15)

        ..  container:: example

            **Example 3.** Inverts named pitch:

            ::

                >>> operator_ = pitchtools.Inversion()
                >>> expr = pitchtools.NamedPitch("d'")
                >>> operator_(expr)
                NamedPitch('bf')

        ..  container:: example

            **Example 4.** Inverts named pitch class:

            ::

                >>> operator_ = pitchtools.Inversion()
                >>> expr = pitchtools.NamedPitchClass('d')
                >>> operator_(expr)
                NamedPitchClass('bf')

        ..  container:: example

            **Example 5.** Inverts pitch segment:

            ::

                >>> operator_ = pitchtools.Inversion()
                >>> expr = pitchtools.PitchSegment("c' d' e'")
                >>> operator_(expr)
                PitchSegment(["c'", 'bf', 'af'])

        ..  container:: example

            **Example 6.** Inverts pitch class segment:

            ::

                >>> operator_ = pitchtools.Inversion()
                >>> expr = pitchtools.PitchClassSegment("c d e")
                >>> operator_(expr)
                PitchClassSegment(['c', 'bf', 'af'])

        ..  container:: example
        
            **Example 7.** Inverts pitch class set:

            ::

                >>> operator_ = pitchtools.Inversion()
                >>> expr = pitchtools.PitchClassSet("c d e")
                >>> operator_(expr)
                PitchClassSet(['c', 'af', 'bf'])

        Returns new object with type equal to that of `expr`.
        '''
        if hasattr(expr, 'invert'):
            result = expr.invert(axis=self.axis)
        else:
            message = 'do not know how to invert: {!r}.'
            message = message.format(expr)
            raise TypeError(message)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def axis(self):
        r'''Gets axis of inversion.

        Returns named pitch or none.
        '''
        return self._axis
