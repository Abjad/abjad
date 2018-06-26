import functools
import itertools
from abjad.system import AbjadValueObject


class Enumerator(AbjadValueObject):
    """
    Enumerator.

    Collects combinatorial enumerator methods.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_sequence',
        )

    ### INITIALIZER ###

    def __init__(self, sequence=None):
        import abjad
        if sequence is not None:
            sequence = abjad.sequence(items=sequence)
        self._sequence = sequence

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_restricted_growth_function(sequence):
        """
        Is true when ``sequence`` is a restricted growth function.

        ..  container:: example

            Is true when sequence is a restricted growth function:

            >>> abjad.Enumerator._is_restricted_growth_function([1, 1, 1, 1])
            True

            >>> abjad.Enumerator._is_restricted_growth_function([1, 1, 1, 2])
            True

            >>> abjad.Enumerator._is_restricted_growth_function([1, 1, 2, 1])
            True

            >>> abjad.Enumerator._is_restricted_growth_function([1, 1, 2, 2])
            True

        ..  container:: example

            Is false when sequence is not a restricted growth function:

            >>> abjad.Enumerator._is_restricted_growth_function([1, 1, 1, 3])
            False

            >>> abjad.Enumerator._is_restricted_growth_function([17])
            False

        A restricted growth function is a sequence ``l`` such that
        ``l[0] == 1`` and such that ``l[i] <= max(l[:i]) + 1`` for
        ``1 <= i <= len(l)``.

        Returns true or false.
        """
        try:
            for i, n in enumerate(sequence):
                if i == 0:
                    if not n == 1:
                        return False
                else:
                    if not n <= max(sequence[:i]) + 1:
                        return False
            return True
        except TypeError:
            return False

    @staticmethod
    def _partition_by_rgf(sequence, rgf):
        """
        Partitions ``sequence`` by restricted growth function ``rgf``.

        >>> sequence = abjad.sequence(range(10))
        >>> rgf = [1, 1, 2, 2, 1, 2, 3, 3, 2, 4]

        >>> abjad.Enumerator._partition_by_rgf(sequence, rgf)
        Sequence([Sequence([0, 1, 4]), Sequence([2, 3, 5, 8]), Sequence([6, 7]), Sequence([9])])

        Returns list of lists.
        """
        import abjad
        rgf = abjad.sequence(items=rgf)
        if not Enumerator._is_restricted_growth_function(rgf):
            message = 'must be restricted growth function: {!r}.'
            message = message.format(rgf)
            raise ValueError(message)
        if not len(sequence) == len(rgf):
            message = 'lengths must be equal.'
            raise ValueError(message)
        partition = []
        for part_index in range(max(rgf)):
            part = []
            partition.append(part)
        for n, part_number in zip(sequence, rgf):
            part_index = part_number - 1
            part = partition[part_index]
            part.append(n)
        partition = [abjad.sequence(_) for _ in partition]
        return abjad.sequence(items=partition)

    @staticmethod
    def _yield_restricted_growth_functions(length):
        """
        Yields restricted growth functions of ``length``.

        ..  container:: example

            >>> rgfs = abjad.Enumerator._yield_restricted_growth_functions(4)
            >>> for rgf in rgfs:
            ...     rgf
            ...
            (1, 1, 1, 1)
            (1, 1, 1, 2)
            (1, 1, 2, 1)
            (1, 1, 2, 2)
            (1, 1, 2, 3)
            (1, 2, 1, 1)
            (1, 2, 1, 2)
            (1, 2, 1, 3)
            (1, 2, 2, 1)
            (1, 2, 2, 2)
            (1, 2, 2, 3)
            (1, 2, 3, 1)
            (1, 2, 3, 2)
            (1, 2, 3, 3)
            (1, 2, 3, 4)

        Returns restricted growth functions in lex order.

        Returns generator of tuples.
        """
        import abjad
        assert abjad.mathtools.is_positive_integer(length), repr(length)
        last_rgf = list(range(1, length + 1))
        rgf = length * [1]
        yield tuple(rgf)
        while not rgf == last_rgf:
            for i, x in enumerate(reversed(rgf)):
                stop = -(i + 1)
                if x < max(rgf[:stop]) + 1:
                    first_part = rgf[:stop]
                    increased_part = [rgf[stop] + 1]
                    trailing_ones = i * [1]
                    rgf = first_part + increased_part + trailing_ones
                    yield tuple(rgf)
                    break

    ### PUBLIC PROPERTIES ###

    @property
    def sequence(self):
        """
        Gets sequence of enumerator.

        Defaults to none.

        Set to sequence or none.

        Returns sequence or none.
        """
        return self._sequence

    ### PUBLIC METHODS ###

    def yield_combinations(self, minimum_length=None, maximum_length=None):
        """
        Yields combinations of sequence items.

        ..  container:: example

            >>> enumerator = abjad.Enumerator([1, 2, 3, 4])
            >>> for combination in enumerator.yield_combinations():
            ...     combination
            Sequence([])
            Sequence([1])
            Sequence([2])
            Sequence([1, 2])
            Sequence([3])
            Sequence([1, 3])
            Sequence([2, 3])
            Sequence([1, 2, 3])
            Sequence([4])
            Sequence([1, 4])
            Sequence([2, 4])
            Sequence([1, 2, 4])
            Sequence([3, 4])
            Sequence([1, 3, 4])
            Sequence([2, 3, 4])
            Sequence([1, 2, 3, 4])

        ..  container:: example

            >>> enumerator = abjad.Enumerator([1, 2, 3, 4])
            >>> for combination in enumerator.yield_combinations(
            ...     minimum_length=3,
            ...     ):
            ...     combination
            Sequence([1, 2, 3])
            Sequence([1, 2, 4])
            Sequence([1, 3, 4])
            Sequence([2, 3, 4])
            Sequence([1, 2, 3, 4])

        ..  container:: example

            >>> enumerator = abjad.Enumerator([1, 2, 3, 4])
            >>> for combination in enumerator.yield_combinations(
            ...     maximum_length=2,
            ...     ):
            ...     combination
            Sequence([])
            Sequence([1])
            Sequence([2])
            Sequence([1, 2])
            Sequence([3])
            Sequence([1, 3])
            Sequence([2, 3])
            Sequence([4])
            Sequence([1, 4])
            Sequence([2, 4])
            Sequence([3, 4])

        ..  container:: example

            >>> enumerator = abjad.Enumerator([1, 2, 3, 4])
            >>> for combination in enumerator.yield_combinations(
            ...     minimum_length=2,
            ...     maximum_length=2,
            ...     ):
            ...     combination
            Sequence([1, 2])
            Sequence([1, 3])
            Sequence([2, 3])
            Sequence([1, 4])
            Sequence([2, 4])
            Sequence([3, 4])

        ..  container:: example

            >>> enumerator = abjad.Enumerator('text')
            >>> for combination in enumerator.yield_combinations():
            ...     ''.join([str(_) for _ in combination])
            ''
            't'
            'e'
            'te'
            'x'
            'tx'
            'ex'
            'tex'
            't'
            'tt'
            'et'
            'tet'
            'xt'
            'txt'
            'ext'
            'text'

        Yields combinations in binary string order.

        Returns sequence generator.
        """
        import abjad
        length = len(self.sequence)
        for i in range(2**length):
            binary_string = abjad.mathtools.integer_to_binary_string(i)
            binary_string = binary_string.zfill(length)
            sublist = []
            for j, digit in enumerate(reversed(binary_string)):
                if digit == '1':
                    sublist.append(self.sequence[j])
            yield_sublist = True
            if minimum_length is not None:
                if len(sublist) < minimum_length:
                    yield_sublist = False
            if maximum_length is not None:
                if maximum_length < len(sublist):
                    yield_sublist = False
            if yield_sublist:
                if isinstance(self.sequence, str):
                    yield ''.join(sublist)
                else:
                    yield abjad.sequence(items=sublist)

    def yield_outer_product(self):
        """
        Yields outer product of sequences in sequence.

        ..  container:: example

            >>> sequences = [[1, 2, 3], ['a', 'b']]
            >>> enumerator = abjad.Enumerator(sequences)
            >>> for sequence_ in enumerator.yield_outer_product():
            ...     sequence_
            ...
            Sequence([1, 'a'])
            Sequence([1, 'b'])
            Sequence([2, 'a'])
            Sequence([2, 'b'])
            Sequence([3, 'a'])
            Sequence([3, 'b'])

        ..  container:: example

            >>> sequences = [[1, 2, 3], ['a', 'b'], ['X', 'Y']]
            >>> enumerator = abjad.Enumerator(sequences)
            >>> for sequence_ in enumerator.yield_outer_product():
            ...     sequence_
            ...
            Sequence([1, 'a', 'X'])
            Sequence([1, 'a', 'Y'])
            Sequence([1, 'b', 'X'])
            Sequence([1, 'b', 'Y'])
            Sequence([2, 'a', 'X'])
            Sequence([2, 'a', 'Y'])
            Sequence([2, 'b', 'X'])
            Sequence([2, 'b', 'Y'])
            Sequence([3, 'a', 'X'])
            Sequence([3, 'a', 'Y'])
            Sequence([3, 'b', 'X'])
            Sequence([3, 'b', 'Y'])

        ..  container:: example

            >>> sequences = [[1, 2, 3], [4, 5], [6, 7, 8]]
            >>> enumerator = abjad.Enumerator(sequences)
            >>> for sequence_ in enumerator.yield_outer_product():
            ...     sequence_
            ...
            Sequence([1, 4, 6])
            Sequence([1, 4, 7])
            Sequence([1, 4, 8])
            Sequence([1, 5, 6])
            Sequence([1, 5, 7])
            Sequence([1, 5, 8])
            Sequence([2, 4, 6])
            Sequence([2, 4, 7])
            Sequence([2, 4, 8])
            Sequence([2, 5, 6])
            Sequence([2, 5, 7])
            Sequence([2, 5, 8])
            Sequence([3, 4, 6])
            Sequence([3, 4, 7])
            Sequence([3, 4, 8])
            Sequence([3, 5, 6])
            Sequence([3, 5, 7])
            Sequence([3, 5, 8])

        Returns sequence generator.
        """
        def _helper(sequence_1, sequence_2):
            result = []
            for item_1 in sequence_1:
                for item_2 in sequence_2:
                    result.extend([item_1 + [item_2]])
            return result
        import abjad
        sequences = [abjad.sequence(_) for _ in self.sequence]
        sequences[0] = [[_] for _ in sequences[0]]
        result = functools.reduce(_helper, sequences)
        for element in result:
            yield abjad.sequence(items=element)

    def yield_pairs(self):
        """
        Yields pairs sequence items.

        ..  container:: example

            Without duplicate items:

            >>> enumerator = abjad.Enumerator([1, 2, 3, 4])
            >>> for pair in enumerator.yield_pairs():
            ...     pair
            ...
            Sequence([1, 2])
            Sequence([1, 3])
            Sequence([1, 4])
            Sequence([2, 3])
            Sequence([2, 4])
            Sequence([3, 4])

        ..  container:: example

            With duplicate items:

            >>> enumerator = abjad.Enumerator([1, 1, 1])
            >>> for pair in enumerator.yield_pairs():
            ...     pair
            ...
            Sequence([1, 1])
            Sequence([1, 1])
            Sequence([1, 1])

        ..  container:: example

            Length-1 sequence:

            >>> enumerator = abjad.Enumerator([1])
            >>> for pair in enumerator.yield_pairs():
            ...     pair
            ...

        ..  container:: example

            Empty sequence:

            >>> enumerator = abjad.Enumerator([])
            >>> for pair in enumerator.yield_pairs():
            ...     pair
            ...

        Returns generator of length-2 sequences.
        """
        import abjad
        for i, item in enumerate(self.sequence):
            start = i + 1
            for item_ in self.sequence[start:]:
                pair = [item, item_]
                yield abjad.sequence(items=pair)

    def yield_partitions(self):
        """
        Yields partitions of sequence.

        ..  container:: example

            >>> enumerator = abjad.Enumerator([0, 1, 2])
            >>> for partition in enumerator.yield_partitions():
            ...     partition
            ...
            Sequence([Sequence([0, 1, 2])])
            Sequence([Sequence([0, 1]), Sequence([2])])
            Sequence([Sequence([0]), Sequence([1, 2])])
            Sequence([Sequence([0]), Sequence([1]), Sequence([2])])

        ..  container:: example

            >>> enumerator = abjad.Enumerator([0, 1, 2, 3])
            >>> for partition in enumerator.yield_partitions():
            ...     partition
            ...
            Sequence([Sequence([0, 1, 2, 3])])
            Sequence([Sequence([0, 1, 2]), Sequence([3])])
            Sequence([Sequence([0, 1]), Sequence([2, 3])])
            Sequence([Sequence([0, 1]), Sequence([2]), Sequence([3])])
            Sequence([Sequence([0]), Sequence([1, 2, 3])])
            Sequence([Sequence([0]), Sequence([1, 2]), Sequence([3])])
            Sequence([Sequence([0]), Sequence([1]), Sequence([2, 3])])
            Sequence([Sequence([0]), Sequence([1]), Sequence([2]), Sequence([3])])

        Returns generator of nested sequences.
        """
        import abjad
        length = len(self.sequence) - 1
        for i in range(2**length):
            binary_string = abjad.mathtools.integer_to_binary_string(i)
            binary_string = binary_string.zfill(length)
            part = list(self.sequence[0:1])
            partition = [part]
            for n, token in zip(self.sequence[1:], binary_string):
                if int(token) == 0:
                    part.append(n)
                else:
                    part = [n]
                    partition.append(part)
            parts = [abjad.sequence(items=_) for _ in partition]
            partition = abjad.sequence(items=parts)
            yield partition

    def yield_permutations(self):
        """
        Yields permutations of sequence.

        ..  container:: example

            >>> enumerator = abjad.Enumerator([1, 2, 3])
            >>> for permutation in enumerator.yield_permutations():
            ...     permutation
            ...
            Sequence([1, 2, 3])
            Sequence([1, 3, 2])
            Sequence([2, 1, 3])
            Sequence([2, 3, 1])
            Sequence([3, 1, 2])
            Sequence([3, 2, 1])

        Returns sequence generator.
        """
        import abjad
        length = len(self.sequence)
        for permutation in itertools.permutations(tuple(range(length))):
            permutation = abjad.sequence(items=permutation)
            yield self.sequence.permute(permutation)

    def yield_set_partitions(self):
        """
        Yields set partitions of sequence.

        ..  container:: example

            >>> enumerator = abjad.Enumerator([21, 22, 23, 24])
            >>> for set_partition in enumerator.yield_set_partitions():
            ...     set_partition
            ...
            Sequence([Sequence([21, 22, 23, 24])])
            Sequence([Sequence([21, 22, 23]), Sequence([24])])
            Sequence([Sequence([21, 22, 24]), Sequence([23])])
            Sequence([Sequence([21, 22]), Sequence([23, 24])])
            Sequence([Sequence([21, 22]), Sequence([23]), Sequence([24])])
            Sequence([Sequence([21, 23, 24]), Sequence([22])])
            Sequence([Sequence([21, 23]), Sequence([22, 24])])
            Sequence([Sequence([21, 23]), Sequence([22]), Sequence([24])])
            Sequence([Sequence([21, 24]), Sequence([22, 23])])
            Sequence([Sequence([21]), Sequence([22, 23, 24])])
            Sequence([Sequence([21]), Sequence([22, 23]), Sequence([24])])
            Sequence([Sequence([21, 24]), Sequence([22]), Sequence([23])])
            Sequence([Sequence([21]), Sequence([22, 24]), Sequence([23])])
            Sequence([Sequence([21]), Sequence([22]), Sequence([23, 24])])
            Sequence([Sequence([21]), Sequence([22]), Sequence([23]), Sequence([24])])

        Returns set partitions in order of restricted growth function.

        Returns generator of list of lists.
        """
        length = len(self.sequence)
        for rgf in Enumerator._yield_restricted_growth_functions(length):
            partition = Enumerator._partition_by_rgf(self.sequence, rgf)
            yield partition

    def yield_subsequences(self, minimum_length=0, maximum_length=None):
        """
        Yields subsequences of ``sequence``.

        ..  container:: example

            >>> enumerator = abjad.Enumerator([0, 1, 2])
            >>> for subsequence in enumerator.yield_subsequences():
            ...     subsequence
            ...
            Sequence([])
            Sequence([0])
            Sequence([0, 1])
            Sequence([0, 1, 2])
            Sequence([1])
            Sequence([1, 2])
            Sequence([2])

        ..  container:: example

            >>> enumerator = abjad.Enumerator([0, 1, 2, 3, 4])
            >>> for subsequence in enumerator.yield_subsequences(
            ...     minimum_length=3,
            ...     ):
            ...     subsequence
            ...
            Sequence([0, 1, 2])
            Sequence([0, 1, 2, 3])
            Sequence([0, 1, 2, 3, 4])
            Sequence([1, 2, 3])
            Sequence([1, 2, 3, 4])
            Sequence([2, 3, 4])

        ..  container:: example

            >>> enumerator = abjad.Enumerator([0, 1, 2, 3, 4])
            >>> for subsequence in enumerator.yield_subsequences(
            ...     maximum_length=3,
            ...     ):
            ...     subsequence
            ...
            Sequence([])
            Sequence([0])
            Sequence([0, 1])
            Sequence([0, 1, 2])
            Sequence([1])
            Sequence([1, 2])
            Sequence([1, 2, 3])
            Sequence([2])
            Sequence([2, 3])
            Sequence([2, 3, 4])
            Sequence([3])
            Sequence([3, 4])
            Sequence([4])

        ..  container:: example

            >>> enumerator = abjad.Enumerator([0, 1, 2, 3, 4])
            >>> for subsequence in enumerator.yield_subsequences(
            ...     minimum_length=3,
            ...     maximum_length=3,
            ...     ):
            ...     subsequence
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])

        Returns sequence generator.
        """
        length = len(self.sequence)
        if maximum_length is None:
            maximum_length = length
        for i in range(length):
            start_j = minimum_length + i
            stop_j = min(maximum_length + i, length) + 1
            for j in range(start_j, stop_j):
                if i < j or i == 0:
                    subsequence = self.sequence[i:j]
                    yield subsequence
