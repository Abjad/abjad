# -*- encoding: utf-8 -*-
import collections
from abjad.tools import mathtools
from abjad.tools.topleveltools import new
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Duplication(AbjadValueObject):
    r'''Duplication operator.

    ..  container:: example:

        ::

            >>> operator_ = sequencetools.Duplication(count=2, period=4)

        ::

            >>> print(format(operator_))
            sequencetools.Duplication(
                count=2,
                period=4,
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_count',
        '_period',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        count=None,
        period=None,
        ):
        if count is not None:
            count = int(count)
            assert 0 <= count
        self._count = count
        if period is not None:
            period = int(period)
            assert 0 < period
        self._period = period

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls rotation on `expr`.

        ..  container:: example

            **Example 1.** Duplicates once without period.

            ::

                >>> operator_ = sequencetools.Duplication(count=1)
                >>> numbers = [1, 2, 3, 4]
                >>> operator_(numbers)
                [1, 2, 3, 4, 1, 2, 3, 4]

        ..  container:: example

            **Example 2.** Duplicates twice without period.

            ::

                >>> operator_ = sequencetools.Duplication(count=2)
                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7])
                >>> operator_(pitch_classes)
                PitchClassSegment([0, 1, 4, 7, 0, 1, 4, 7, 0, 1, 4, 7])

        ..  container:: example

            **Example 3.** Duplicates periodically.

            ::

                >>> operator_ = sequencetools.Duplication(count=1, period=3)
                >>> pitches = pitchtools.PitchSegment("c' d' e' f' g' a' b' c''")
                >>> for pitch in operator_(pitches):
                ...     pitch
                ...
                NamedPitch("c'")
                NamedPitch("d'")
                NamedPitch("e'")
                NamedPitch("c'")
                NamedPitch("d'")
                NamedPitch("e'")
                NamedPitch("f'")
                NamedPitch("g'")
                NamedPitch("a'")
                NamedPitch("f'")
                NamedPitch("g'")
                NamedPitch("a'")
                NamedPitch("b'")
                NamedPitch("c''")
                NamedPitch("b'")
                NamedPitch("c''")

        Returns new object with type equal to that of `expr`.
        '''
        from abjad.tools import datastructuretools
        from abjad.tools import sequencetools
        if not isinstance(expr, collections.Sequence):
            expr = (expr,)
        count = (self.count or 1) + 1
        if not self.period:
            return type(expr)(expr * count)
        if isinstance(expr, datastructuretools.TypedCollection):
            result = new(expr, items=())
        else:
            result = type(expr)()
        for shard in sequencetools.partition_sequence_by_counts(
            expr,
            [self.period],
            cyclic=True,
            overhang=True,
            ):
            shard = type(expr)(shard) * count
            result = result + shard
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def count(self):
        r'''Gets count of duplication.

        ..  container:: example

            ::

                >>> operator_ = sequencetools.Duplication(count=1, period=3)
                >>> operator_.count
                1

        Returns integer or none.
        '''
        return self._count

    @property
    def period(self):
        r'''Gets period of duplication.

        ..  container:: example

            ::

                >>> operator_ = sequencetools.Duplication(count=1, period=3)
                >>> operator_.period
                3

        Returns integer or none.
        '''
        return self._period
