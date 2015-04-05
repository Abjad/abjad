# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Retrogression(AbjadValueObject):
    r'''Retrogression operator.

    ..  container:: example:

        ::

            >>> operator_ = pitchtools.Retrogression()

        ::

            >>> print(format(operator_))
            pitchtools.Retrogression()

    Object model of the twelve-tone retrogression operator.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_period',
        )

    ### INITIALIZER ###

    def __init__(self, period=None):
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls retrogression on `expr`.

        ..  container:: example

            **Example 1.** Retrograde pitch classes.

            ::

                >>> operator_ = pitchtools.Retrogression()
                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7])
                >>> operator_(pitch_classes)
                PitchClassSegment([7, 4, 1, 0])

        ..  container:: example

            **Example 2.** Does not retrograde single pitches or pitch-classes.

            ::

                >>> operator_ = pitchtools.Retrogression()
                >>> pitch_class = pitchtools.NumberedPitchClass(6)
                >>> operator_(pitch_class)
                NumberedPitchClass(6)

        Returns new object with type equal to that of `expr`.
        '''
        from abjad.tools import pitchtools
        if isinstance(expr, (pitchtools.Pitch, pitchtools.PitchClass)):
            return expr
        if not isinstance(expr, (
            pitchtools.PitchSegment,
            pitchtools.PitchClassSegment,
            )):
            expr = pitchtools.PitchSegment(expr)
        return type(expr)(reversed(expr))

    ### PUBLIC PROPERTIES ###

    @property
    def period(self):
        r'''Gets optional period of retrogression.

        ..  container:: example

            ::

                >>> operator_ = pitchtools.Retrogression(period=3)
                >>> operator_.period
                3

        Returns integer or none.
        '''
        return self._period
