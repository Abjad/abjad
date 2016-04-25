# -*- coding: utf-8 -*-
import collections
from abjad.tools.topleveltools import new
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Duplication(AbjadValueObject):
    r'''Duplication operator.

    ..  container:: example:

        ::

            >>> operator_ = sequencetools.Duplication(counts=2, period=4)

        ::

            >>> print(format(operator_))
            sequencetools.Duplication(
                counts=2,
                period=4,
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_counts',
        '_indices',
        '_period',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        counts=None,
        indices=None,
        period=None,
        ):
        if counts is not None:
            if isinstance(counts, collections.Sequence):
                assert len(counts)
                counts = tuple(int(_) for _ in counts)
                assert all(0 <= _ for _ in counts)
            else:
                counts = int(counts)
                assert 0 <= counts
        self._counts = counts
        if indices is not None:
            assert all(isinstance(_, int) for _ in indices), repr(indices)
            indices = tuple(indices)
        self._indices = indices
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

                >>> operator_ = sequencetools.Duplication(counts=1)
                >>> numbers = [1, 2, 3, 4]
                >>> operator_(numbers)
                [1, 2, 3, 4, 1, 2, 3, 4]

        ..  container:: example

            **Example 2.** Duplicates twice without period.

            ::

                >>> operator_ = sequencetools.Duplication(counts=2)
                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7])
                >>> operator_(pitch_classes)
                PitchClassSegment([0, 1, 4, 7, 0, 1, 4, 7, 0, 1, 4, 7])

        ..  container:: example

            **Example 3.** Duplicates periodically.

            ::

                >>> operator_ = sequencetools.Duplication(counts=1, period=3)
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

        ..  container:: example

            **Example 4.** Duplicate indices.

            ::

                >>> operator_ = sequencetools.Duplication(
                ...     counts=1,
                ...     indices=(0, -1),
                ...     )
                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7])
                >>> operator_(pitch_classes)
                PitchClassSegment([0, 0, 1, 4, 7, 7])

        ..  container:: example

            **Example 5.** Duplicate indices periodically.

            ::

                >>> operator_ = sequencetools.Duplication(
                ...     counts=1,
                ...     indices=(0,),
                ...     period=2,
                ...     )
                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7, 9])
                >>> operator_(pitch_classes)
                PitchClassSegment([0, 0, 1, 4, 4, 7, 9, 9])

        ..  container:: example

            **Example 6.** Duplicate indices periodically with different
            counts.

            ::

                >>> operator_ = sequencetools.Duplication(
                ...     counts=(1, 2),
                ...     indices=(0,),
                ...     period=2,
                ...     )
                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7, 9])
                >>> operator_(pitch_classes)
                PitchClassSegment([0, 0, 1, 4, 4, 4, 7, 9, 9])

        ..  container:: example

            **Example 7.** Cyclic counts.

            ::

                >>> operator_ = sequencetools.Duplication(counts=(0, 1, 2, 3))
                >>> pitch_classes = pitchtools.PitchClassSegment([0, 1, 4, 7, 9])
                >>> operator_(pitch_classes)
                PitchClassSegment([0, 1, 1, 4, 4, 4, 7, 7, 7, 7, 9])
                
        Returns new object with type equal to that of `expr`.
        '''
        from abjad.tools import datastructuretools
        from abjad.tools import patterntools
        from abjad.tools import sequencetools

        if not isinstance(expr, collections.Sequence):
            expr = (expr,)

        counts = self.counts
        if isinstance(counts, int):
            counts = counts + 1
        else:
            counts = [_ + 1 for _ in counts]

        if not self.period and not self.indices:
            if isinstance(counts, int):
                return type(expr)(expr * counts)
            else:
                counts = datastructuretools.CyclicTuple(counts)
                result = []
                for i, x in enumerate(expr):
                    count = counts[i]
                    result.extend([x] * count)
                if isinstance(expr, datastructuretools.TypedCollection):
                    result = new(expr, items=result)
                else:
                    result = type(expr)(result)
                return result

        if isinstance(counts, int):
            counts = [counts]
        counts = datastructuretools.CyclicTuple(counts)

        if not self.indices:
            if isinstance(expr, datastructuretools.TypedCollection):
                result = new(expr, items=())
            else:
                result = type(expr)()
            iterator = sequencetools.partition_sequence_by_counts(
                expr, [self.period], cyclic=True, overhang=True)
            for i, shard in enumerate(iterator):
                shard = type(expr)(shard) * counts[i]
                result = result + shard
            return result

        pattern = patterntools.Pattern(
            indices=self.indices,
            period=self.period,
            )
        result = []
        length = len(expr)
        j = 0
        for i, x in enumerate(expr):
            if pattern.matches_index(i, length):
                count = counts[j]
                result.extend([x] * count)
                j += 1
            else:
                result.append(x)
        if isinstance(expr, datastructuretools.TypedCollection):
            result = new(expr, items=result)
        else:
            result = type(expr)(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts of duplication.

        ..  container:: example

            ::

                >>> operator_ = sequencetools.Duplication(counts=1, period=3)
                >>> operator_.counts
                1

        Returns integer or none.
        '''
        return self._counts

    @property
    def indices(self):
        r'''Gets indices of duplication.

        ..  container:: example

            ::

                >>> operator_ = sequencetools.Duplication(
                ...     counts=1,
                ...     indices=(0, -1),
                ...     )
                >>> operator_.indices
                (0, -1)

        Returns integer or none.
        '''
        return self._indices

    @property
    def period(self):
        r'''Gets period of duplication.

        ..  container:: example

            ::

                >>> operator_ = sequencetools.Duplication(counts=1, period=3)
                >>> operator_.period
                3

        Returns integer or none.
        '''
        return self._period
