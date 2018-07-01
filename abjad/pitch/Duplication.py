import collections
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.utilities.CyclicTuple import CyclicTuple


class Duplication(AbjadValueObject):
    """
    Duplication.

    ..  container:: example:

        >>> operator_ = abjad.Duplication(counts=2, period=4)

        >>> abjad.f(operator_)
        abjad.Duplication(
            counts=2,
            period=4,
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_counts',
        '_indices',
        '_period',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
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

    def __call__(self, argument):
        """
        Calls rotation on `argument`.

        ..  container:: example

            Duplicates once without period:

            >>> operator_ = abjad.Duplication(counts=1)
            >>> numbers = [1, 2, 3, 4]
            >>> operator_(numbers)
            [1, 2, 3, 4, 1, 2, 3, 4]

        ..  container:: example

            Duplicates twice without period:

            >>> operator_ = abjad.Duplication(counts=2)
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 1, 4, 7, 0, 1, 4, 7, 0, 1, 4, 7])

        ..  container:: example

            Duplicates periodically:

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> pitches = abjad.PitchSegment("c' d' e' f' g' a' b' c''")
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

            Duplicate indices:

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0, -1),
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 0, 1, 4, 7, 7])

        ..  container:: example

            Duplicate indices periodically:

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0,),
            ...     period=2,
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 0, 1, 4, 4, 7, 9, 9])

        ..  container:: example

            Duplicate indices periodically with different counts:

            >>> operator_ = abjad.Duplication(
            ...     counts=(1, 2),
            ...     indices=(0,),
            ...     period=2,
            ...     )
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 0, 1, 4, 4, 4, 7, 9, 9])

        ..  container:: example

            Cyclic counts:

            >>> operator_ = abjad.Duplication(counts=(0, 1, 2, 3))
            >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7, 9])
            >>> operator_(pitch_classes)
            PitchClassSegment([0, 1, 1, 4, 4, 4, 7, 7, 7, 7, 9])

        Returns new object with type equal to that of `argument`.
        """
        import abjad

        if not isinstance(argument, collections.Sequence):
            argument = (argument,)

        counts = self.counts
        if isinstance(counts, int):
            counts = counts + 1
        else:
            counts = [_ + 1 for _ in counts]

        if not self.period and not self.indices:
            if isinstance(counts, int):
                return type(argument)(argument * counts)
            else:
                counts = CyclicTuple(counts)
                result = []
                for i, x in enumerate(argument):
                    count = counts[i]
                    result.extend([x] * count)
                if isinstance(argument, abjad.TypedCollection):
                    result = abjad.new(argument, items=result)
                else:
                    result = type(argument)(result)
                return result

        if isinstance(counts, int):
            counts = [counts]
        counts = CyclicTuple(counts)

        if not self.indices:
            if isinstance(argument, abjad.TypedCollection):
                result = abjad.new(argument, items=())
            else:
                result = type(argument)()
            iterator = abjad.sequence(argument).partition_by_counts(
                [self.period],
                cyclic=True,
                overhang=True,
                )
            for i, shard in enumerate(iterator):
                shard = type(argument)(shard) * counts[i]
                result = result + shard
            return result

        pattern = abjad.Pattern(
            indices=self.indices,
            period=self.period,
            )
        result = []
        length = len(argument)
        j = 0
        for i, x in enumerate(argument):
            if pattern.matches_index(i, length):
                count = counts[j]
                result.extend([x] * count)
                j += 1
            else:
                result.append(x)
        if isinstance(argument, abjad.TypedCollection):
            result = abjad.new(argument, items=result)
        else:
            result = type(argument)(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        """
        Gets counts of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> operator_.counts
            1

        Returns integer or none.
        """
        return self._counts

    @property
    def indices(self):
        """
        Gets indices of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(
            ...     counts=1,
            ...     indices=(0, -1),
            ...     )
            >>> operator_.indices
            (0, -1)

        Returns integer or none.
        """
        return self._indices

    @property
    def period(self):
        """
        Gets period of duplication.

        ..  container:: example

            >>> operator_ = abjad.Duplication(counts=1, period=3)
            >>> operator_.period
            3

        Returns integer or none.
        """
        return self._period
