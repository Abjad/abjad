# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class Rotation(AbjadObject):
    r'''Rotation operator.

    ..  container:: example:

        ::

            >>> operator_ = pitchtools.Rotation(1)

        ::

            >>> print(format(operator_))
            pitchtools.Rotation(
                index=1,
                transpose=True,
                )

    Object model of the twelve-tone rotation operator.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_index',
        '_transpose',
        )

    ### INITIALIZER ###

    def __init__(self, index=0, transpose=True):
        self._index = int(index)
        self._transpose = bool(transpose)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls rotation on `expr`.

        ..  container:: example

            **Example 1.** Rotates pitch classes with transposition.

            ::

                >>> operator_ = pitchtools.Rotation(index=1)
                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7])
                >>> operator_(pitch_classes)
                PitchClassSegment([0, 5, 6, 9])

        ..  container:: example

            **Example 2.** Rotates pitch classes without transposition.

            ::

                >>> operator_ = pitchtools.Rotation(index=1, transpose=False)
                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7])
                >>> operator_(pitch_classes)
                PitchClassSegment([7, 0, 1, 4])

        ..  container:: example

            **Example 3.** Does not rotate single pitches or pitch-classes.

            ::

                >>> operator_ = pitchtools.Rotation(index=1)
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
        return expr.rotate(self.index, transpose=self.transpose)

    ### PUBLIC METHODS ###

    @property
    def index(self):
        r'''Gets index of rotation.

        ..  container:: example

            ::

                >>> operator_ = pitchtools.Rotation(index=2)
                >>> operator_.index
                2

        Returns integer.
        '''
        return self._index

    @property
    def transpose(self):
        r'''Is true if rotation transposes its output to the original starting
        pitch of its unrotated input.

        ..  container:: example

            ::

                >>> operator_ = pitchtools.Rotation(index=2, transpose=False)
                >>> operator_.transpose
                False

        Returns boolean.
        '''
        return self._transpose