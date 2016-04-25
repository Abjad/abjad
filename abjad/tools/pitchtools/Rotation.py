# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.topleveltools import new
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Rotation(AbjadValueObject):
    r'''Rotation operator.

    ..  container:: example:

        **Example.**

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
        '_period',
        )

    ### INITIALIZER ###

    def __init__(self, index=0, transpose=True, period=None):
        self._index = int(index)
        self._transpose = bool(transpose)
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period

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

        ..  container:: example

            **Example 4.** Periodic rotation without transposition.

            ::

                >>> operator_ = pitchtools.Rotation(
                ...     index=1,
                ...     period=3,
                ...     transpose=False,
                ...     )
                >>> pitches = pitchtools.PitchSegment("c' d' e' f' g' a' b' c''")
                >>> operator_(pitches)
                PitchSegment(["e'", "c'", "d'", "a'", "f'", "g'", "c''", "b'"])

        ..  container:: example

            **Example 5.** Periodic rotation with transposition.

            ::

                >>> operator_ = pitchtools.Rotation(
                ...     index=1,
                ...     period=3,
                ...     )
                >>> pitches = pitchtools.PitchSegment("c' d' e' f' g' a' b' c''")
                >>> operator_(pitches)
                PitchSegment(["c'", 'af', 'bf', "f'", "df'", "ef'", "b'", "as'"])

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
        if not self.period:
            return expr.rotate(self.index, transpose=self.transpose)
        result = new(expr, items=())
        for shard in sequencetools.partition_sequence_by_counts(
            expr,
            [self.period],
            cyclic=True,
            overhang=True,
            ):
            shard = type(expr)(shard)
            shard = shard.rotate(self.index, transpose=self.transpose)
            result = result + shard
        return result

    ### PUBLIC PROPERTIES ###

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
    def period(self):
        r'''Gets period of rotation.

        ..  container:: example

            ::

                >>> operator_ = pitchtools.Rotation(index=2, period=3)
                >>> operator_.period
                3

        Returns integer or none.
        '''
        return self._period

    @property
    def transpose(self):
        r'''Is true if rotation transposes its output to the original starting
        pitch of its unrotated input.

        ..  container:: example

            ::

                >>> operator_ = pitchtools.Rotation(index=2, transpose=False)
                >>> operator_.transpose
                False

        Returns true or false.
        '''
        return self._transpose
