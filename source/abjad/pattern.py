import collections
import dataclasses
import operator as operator_module
import typing

from . import math as _math


@dataclasses.dataclass(slots=True)
class Pattern:
    """
    Pattern.

    ..  container:: example

        Matches three indices out of every eight:

        >>> pattern = abjad.Pattern(
        ...     indices=[0, 1, 7],
        ...     period=8,
        ... )

        >>> total_length = 16
        >>> for index in range(16):
        ...     match = pattern.matches_index(index, total_length)
        ...     match = match or ''
        ...     print(index, match)
        0 True
        1 True
        2
        3
        4
        5
        6
        7 True
        8 True
        9 True
        10
        11
        12
        13
        14
        15 True

    ..  container:: example

        Matches three indices out of every sixteen:

        >>> pattern = abjad.Pattern(
        ...     indices=[0, 1, 7],
        ...     period=16,
        ... )

        >>> total_length = 16
        >>> for index in range(16):
        ...     match = pattern.matches_index(index, total_length)
        ...     match = match or ''
        ...     print(index, match)
        0 True
        1 True
        2
        3
        4
        5
        6
        7 True
        8
        9
        10
        11
        12
        13
        14
        15

    ..  container:: example

        Works with improper indices:

        >>> pattern = abjad.Pattern(
        ...     indices=[16, 17, 23],
        ...     period=16,
        ... )

        >>> total_length = 16
        >>> for index in range(16):
        ...     match = pattern.matches_index(index, total_length)
        ...     match = match or ''
        ...     print(index, match)
        0 True
        1 True
        2
        3
        4
        5
        6
        7 True
        8
        9
        10
        11
        12
        13
        14
        15

    ..  container:: example

        Sieve from opening of Xenakis's Psappha:

        >>> sieve_1a = abjad.index([0, 1, 7], 8)
        >>> sieve_1b = abjad.index([1, 3], 5)
        >>> sieve_1 = sieve_1a & sieve_1b
        >>> sieve_2a = abjad.index([0, 1, 2], 8)
        >>> sieve_2b = abjad.index([0], 5)
        >>> sieve_2 = sieve_2a & sieve_2b
        >>> sieve_3 = abjad.index([3], 8)
        >>> sieve_4 = abjad.index([4], 8)
        >>> sieve_5a = abjad.index([5, 6], 8)
        >>> sieve_5b = abjad.index([2, 3, 4], 5)
        >>> sieve_5 = sieve_5a & sieve_5b
        >>> sieve_6a = abjad.index([1], 8)
        >>> sieve_6b = abjad.index([2], 5)
        >>> sieve_6 = sieve_6a & sieve_6b
        >>> sieve_7a = abjad.index([6], 8)
        >>> sieve_7b = abjad.index([1], 5)
        >>> sieve_7 = sieve_7a & sieve_7b
        >>> sieve = sieve_1 | sieve_2 | sieve_3 | sieve_4 | sieve_5 | sieve_6 | sieve_7

        >>> sieve.get_boolean_vector(total_length=40)
        [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
        1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]

    ..  container:: example

        Inverted works like this:

        Matches three indices out of every eight:

        >>> pattern = abjad.Pattern(
        ...     indices=[0, 1, 7],
        ...     period=8,
        ... )

        >>> pattern.inverted is None
        True

        >>> total_length = 16
        >>> for index in range(16):
        ...     match = pattern.matches_index(index, total_length)
        ...     match = match or ''
        ...     print(index, match)
        0 True
        1 True
        2
        3
        4
        5
        6
        7 True
        8 True
        9 True
        10
        11
        12
        13
        14
        15 True

        Pattern that rejects three indices from every eight; equivalently, pattern
        matches ``8-3=5`` indices out of every eight:

        >>> pattern = abjad.Pattern(
        ...     indices=[0, 1, 7],
        ...     period=8,
        ...     inverted=True
        ... )

        >>> pattern.inverted
        True

        >>> total_length = 16
        >>> for index in range(16):
        ...     match = pattern.matches_index(index, total_length)
        ...     match = match or ''
        ...     print(index, match)
        0
        1
        2 True
        3 True
        4 True
        5 True
        6 True
        7
        8
        9
        10 True
        11 True
        12 True
        13 True
        14 True
        15

        Matches every index that is (one of the first three indices) OR (one of the last
        three indices):

        >>> pattern_1 = abjad.index_first(3)
        >>> pattern_2 = abjad.index_last(3)
        >>> pattern = pattern_1 | pattern_2
        >>> pattern.inverted is None
        True

        >>> pattern.get_boolean_vector(total_length=16)
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

        Matches every index that is NOT (one of the first three indices) OR (one of the
        last three indices):

        >>> import dataclasses
        >>> pattern = dataclasses.replace(pattern, inverted=True)
        >>> pattern.inverted
        True

        >>> pattern.get_boolean_vector(total_length=16)
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

    ..  container:: example

        Payload works like this: Pattern with string payload assigned to three of every
        eight indices:

        >>> pattern = abjad.Pattern(
        ...     indices=[0, 1, 7],
        ...     payload='Allegro non troppo',
        ...     period=8,
        ... )

        >>> total_length = 10
        >>> for index in range(10):
        ...     match = pattern.matches_index(index, total_length)
        ...     if match:
        ...         payload = pattern.payload
        ...     else:
        ...         payload = ''
        ...     print(index, repr(payload))
        ...
        0 'Allegro non troppo'
        1 'Allegro non troppo'
        2 ''
        3 ''
        4 ''
        5 ''
        6 ''
        7 'Allegro non troppo'
        8 'Allegro non troppo'
        9 'Allegro non troppo'

    ..  container:: example

        Period works like this:

        Pattern with a period of eight:

        >>> pattern = abjad.Pattern(
        ...     indices=[0, 1, 7],
        ...     period=8,
        ... )

        >>> pattern.period
        8

        >>> total_length = 16
        >>> for index in range(16):
        ...     match = pattern.matches_index(index, total_length)
        ...     match = match or ''
        ...     print(index, match)
        0 True
        1 True
        2
        3
        4
        5
        6
        7 True
        8 True
        9 True
        10
        11
        12
        13
        14
        15 True

        Same pattern with a period of sixteen:

        >>> pattern = abjad.Pattern(
        ...     indices=[0, 1, 7],
        ...     period=16,
        ... )

        >>> pattern.period
        16

        >>> total_length = 16
        >>> for index in range(16):
        ...     match = pattern.matches_index(index, total_length)
        ...     match = match or ''
        ...     print(index, match)
        0 True
        1 True
        2
        3
        4
        5
        6
        7 True
        8
        9
        10
        11
        12
        13
        14
        15

        Gets period of pattern that indexs every fourth and fifth element:

        >>> pattern_1 = abjad.Pattern([0], period=4)
        >>> pattern_2 = abjad.Pattern([0], period=5)
        >>> pattern = pattern_1 | pattern_2
        >>> pattern
        Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=4), Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=5)), payload=None, period=20)

        >>> pattern.period
        20

        Returns none when pattern contains acyclic parts:

        >>> pattern_1 = abjad.Pattern([0], period=4)
        >>> pattern_2 = abjad.Pattern([0])
        >>> pattern = pattern_1 | pattern_2
        >>> pattern
        Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=4), Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

        >>> pattern.period is None
        True

    """

    indices: typing.Any = None
    inverted: typing.Any = None
    operator: typing.Any = None
    patterns: typing.Any = None
    payload: typing.Any = None
    period: typing.Any = None

    _name_to_operator = {
        "and": operator_module.and_,
        "or": operator_module.or_,
        "xor": operator_module.xor,
    }

    def __post_init__(self):
        if self.indices is not None:
            assert all(isinstance(_, int) for _ in self.indices), repr(self.indices)
            self.indices = tuple(self.indices)
        if self.inverted is not None:
            self.inverted = bool(self.inverted)
        if self.operator is not None:
            assert self.operator in self._name_to_operator, repr(self.operator)
        if self.patterns is not None:
            assert all(isinstance(_, type(self)) for _ in self.patterns)
            self.patterns = tuple(self.patterns)
        if self.period is None:
            if self.patterns:
                periods = [_.period for _ in self.patterns]
                if None not in periods:
                    self.period = _math.least_common_multiple(*periods)
        if self.period is not None:
            assert _math.is_positive_integer(self.period), repr(self.period)

    ### SPECIAL METHODS ###

    def __and__(self, pattern):
        """
        Logical AND of two patterns.

        ..  container:: example

            Flat grouping of two patterns:

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern_1 & pattern_2
            Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

        ..  container:: example

            Flat grouping of three patterns:

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern_3 = abjad.index([0], 2)
            >>> pattern = pattern_1 & pattern_2 & pattern_3
            >>> pattern
            Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=2)), payload=None, period=None)

            >>> pattern.get_boolean_vector(total_length=16)
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ..  container:: example

            Nested grouping of three patterns:

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern_3 = abjad.index([0], 2)
            >>> pattern = pattern_1 & pattern_2 | pattern_3
            >>> pattern
            Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None), Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=2)), payload=None, period=None)

            >>> pattern.get_boolean_vector(total_length=16)
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

        ..  container:: example

            In-place AND is allowed:

            >>> pattern = abjad.index_first(3)
            >>> pattern &= abjad.index_last(3)
            >>> pattern
            Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

        Returns new pattern.
        """
        if self._can_append_to_self(pattern, "and"):
            if self.patterns is None:
                self_patterns = [self]
            else:
                self_patterns = list(self.patterns)
            patterns = self_patterns + [pattern]
            result = type(self)(operator="and", patterns=patterns)
        else:
            result = type(self)(operator="and", patterns=[self, pattern])
        return result

    def __invert__(self):
        """
        Inverts pattern.

        ..  container:: example

            >>> pattern = abjad.index_first(3)
            >>> pattern
            Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None)

            >>> pattern = ~pattern
            >>> pattern
            Pattern(indices=(0, 1, 2), inverted=True, operator=None, patterns=None, payload=None, period=None)

            >>> pattern = ~pattern
            >>> pattern
            Pattern(indices=(0, 1, 2), inverted=False, operator=None, patterns=None, payload=None, period=None)

            Negation defined equal to inversion.

        ..  container:: example

            Matches every index that is (one of the first three indices) or (one of the
            last three indices):

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern = pattern_1 | pattern_2
            >>> pattern
            Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

            >>> pattern.get_boolean_vector(total_length=16)
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

        ..  container:: example

            Matches every index that is NOT (one of the first three indices) or
            (one of the last three indices):

            >>> pattern = ~pattern
            >>> pattern
            Pattern(indices=None, inverted=True, operator='or', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

            >>> pattern.get_boolean_vector(total_length=16)
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

        Returns new pattern.
        """
        inverted = not self.inverted
        return dataclasses.replace(self, inverted=inverted)

    def __len__(self):
        """
        Gets length of pattern.

        ..  container:: example

            Gets length of cyclic pattern:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ... )

            >>> len(pattern)
            8

            Length of cyclic pattern defined equal to period of the pattern.

        ..  container:: example

            Gets length of acyclic pattern:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 2, 3],
            ... )

            >>> len(pattern)
            4

            Length of acyclic pattern defined equal to greatest index in
            pattern, plus 1.

        ..  container:: example

            Gets length of pattern with negative indices:

            >>> pattern = abjad.Pattern(
            ...     indices=[-3],
            ... )

            >>> len(pattern)
            3

            Length of pattern with negative indices defined equal to absolute
            value of least index.

        Returns nonnegative integer.
        """
        if self.period is not None:
            return self.period
        if self.indices:
            absolute_indices = []
            for index in self.indices:
                if 0 <= index:
                    absolute_indices.append(index)
                else:
                    index = abs(index) - 1
                    absolute_indices.append(index)
            maximum_index = max(absolute_indices)
            return maximum_index + 1
        return 0

    def __or__(self, pattern):
        """
        Logical OR of two patterns.

        ..  container:: example

            Flat grouping of two patterns:

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern = pattern_1 | pattern_2
            >>> pattern
            Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

        ..  container:: example

            Flat grouping:

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern_3 = abjad.index([0], 2)
            >>> pattern = pattern_1 | pattern_2 | pattern_3
            >>> pattern
            Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=2)), payload=None, period=None)

            >>> pattern.get_boolean_vector(total_length=16)
            [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]

        ..  container:: example

            Nested grouping:

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern_3 = abjad.index([0], 2)
            >>> pattern = pattern_1 | pattern_2 & pattern_3
            >>> pattern
            Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=2)), payload=None, period=None)), payload=None, period=None)

            >>> pattern.get_boolean_vector(total_length=16)
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

        ..  container:: example

            In-place OR is allowed:

            >>> pattern = abjad.index_first(3)
            >>> pattern |= abjad.index_last(3)
            >>> pattern
            Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

        Returns new pattern.
        """
        if self._can_append_to_self(pattern, "or"):
            if self.patterns is None:
                self_patterns = [self]
            else:
                self_patterns = list(self.patterns)
            patterns = self_patterns + [pattern]
            result = type(self)(operator="or", patterns=patterns)
        else:
            result = type(self)(operator="or", patterns=[self, pattern])
        return result

    def __xor__(self, pattern):
        """
        Logical XOR of two patterns.

        ..  container:: example

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern = pattern_1 ^ pattern_2
            >>> pattern
            Pattern(indices=None, inverted=None, operator='xor', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

        ..  container:: example

            Flat grouping:

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern_3 = abjad.index([0], 2)
            >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
            >>> pattern
            Pattern(indices=None, inverted=None, operator='xor', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=2)), payload=None, period=None)

            >>> pattern.get_boolean_vector(total_length=16)
            [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]

        ..  container:: example

            Nested grouping:

            >>> pattern_1 = abjad.index_first(3)
            >>> pattern_2 = abjad.index_last(3)
            >>> pattern_3 = abjad.index([0], 2)
            >>> pattern = pattern_1 ^ pattern_2 & pattern_3
            >>> pattern
            Pattern(indices=None, inverted=None, operator='xor', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=2)), payload=None, period=None)), payload=None, period=None)

            >>> pattern.get_boolean_vector(total_length=16)
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

        ..  container:: example

            In-place XOR is allowed:

            >>> pattern = abjad.index_first(3)
            >>> pattern ^= abjad.index_last(3)
            >>> pattern
            Pattern(indices=None, inverted=None, operator='xor', patterns=(Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

        Returns new pattern.
        """
        if self._can_append_to_self(pattern, "xor"):
            if self.patterns is None:
                self_patterns = [self]
            else:
                self_patterns = list(self.patterns)
            patterns = self_patterns + [pattern]
            result = type(self)(operator="xor", patterns=patterns)
        else:
            result = type(self)(operator="xor", patterns=[self, pattern])
        return result

    ### PRIVATE METHODS ###

    def _can_append_to_self(self, pattern, operator_):
        if not isinstance(pattern, type(self)):
            return False
        if self.operator is None:
            return True
        if self.operator == operator_ and (
            pattern.operator is None or (pattern.operator == self.operator)
        ):
            return True
        return False

    def _make_subscript_string(self):
        return str(self)

    @property
    def weight(self):
        """
        Gets weight of pattern.

        ..  container:: example

            Gets weight of cyclic pattern:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ... )

            >>> pattern.weight
            3

        ..  container:: example

            Gets weight of acyclic pattern:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 2, 3],
            ... )

            >>> pattern.weight
            3

        Weight defined equal to number of indices in pattern.

        Returns nonnegative integer.
        """
        return len(self.indices)

    ### PUBLIC METHODS ###

    def advance(self, count: int | None = None) -> "Pattern":
        """
        Advances pattern.

        ..  container:: example

            >>> pattern = abjad.Pattern([0, 2, 12])

            >>> pattern = pattern.advance(8)
            >>> pattern
            Pattern(indices=(4,), inverted=None, operator=None, patterns=None, payload=None, period=None)

            >>> pattern = pattern.advance(8)
            >>> pattern
            Pattern(indices=(), inverted=None, operator=None, patterns=None, payload=None, period=None)

        ..  container:: example

            Returns copy of pattern when count is none:

            >>> pattern = abjad.Pattern([0, 2, 12])
            >>> pattern.advance()
            Pattern(indices=(0, 2, 12), inverted=None, operator=None, patterns=None, payload=None, period=None)

        ..  container:: example exception

            Raises exception on attempt to advance negative pattern:

            >>> pattern = abjad.Pattern([-2, -1])
            >>> pattern.advance(8)
            Traceback (most recent call last):
                ...
            Exception: can not advance pattern with negative indices ...

        """
        if not count:
            return dataclasses.replace(self)
        assert 0 < count, repr(count)
        for index in self.indices:
            if index < 0:
                message = "can not advance pattern"
                message += f" with negative indices ({repr(self)})."
                raise Exception(message)
        new_indices = []
        for index in self.indices:
            new_index = index - count
            if 0 <= new_index:
                new_indices.append(new_index)
        return dataclasses.replace(self, indices=new_indices)

    @classmethod
    def from_vector(class_, vector):
        """
        Makes pattern from boolean ``vector``.

        ..  container:: example

            Matches three indices out of every five:

            >>> pattern = [1, 0, 0, 1, 1]
            >>> pattern = abjad.Pattern.from_vector(pattern)
            >>> pattern
            Pattern(indices=(0, 3, 4), inverted=None, operator=None, patterns=None, payload=None, period=5)

            >>> total_length = 10
            >>> for index in range(10):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1
            2
            3 True
            4 True
            5 True
            6
            7
            8 True
            9 True

        ..  container:: example

            Matches three indices out of every six:

            >>> pattern = [1, 0, 0, 1, 1, 0]
            >>> pattern = abjad.Pattern.from_vector(pattern)
            >>> pattern
            Pattern(indices=(0, 3, 4), inverted=None, operator=None, patterns=None, payload=None, period=6)

            >>> total_length = 12
            >>> for index in range(12):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1
            2
            3 True
            4 True
            5
            6 True
            7
            8
            9 True
            10 True
            11

        Returns pattern.
        """
        vector = [bool(_) for _ in vector]
        period = len(vector)
        indices = [i for i, x in enumerate(vector) if x]
        return class_(period=period, indices=indices)

    def get_boolean_vector(self, total_length=None):
        """
        Gets boolean vector of pattern applied to input sequence with
        ``total_length``.

        ..  container:: example

            Gets boolean vector of acyclic pattern:

            >>> pattern = abjad.Pattern(
            ...     indices=[4, 5, 6, 7],
            ... )


            >>> pattern.get_boolean_vector(4)
            [0, 0, 0, 0]

            >>> pattern.get_boolean_vector(8)
            [0, 0, 0, 0, 1, 1, 1, 1]

            >>> pattern.get_boolean_vector(16)
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

            Sets total length to length of pattern when ``total_length`` is
            none:

            >>> pattern.get_boolean_vector()
            [0, 0, 0, 0, 1, 1, 1, 1]

        ..  container:: example

            Gets vector of cyclic pattern:

            >>> pattern = abjad.Pattern(
            ...     indices=[4, 5, 6, 7],
            ...     period=20,
            ... )

            >>> pattern.get_boolean_vector(4)
            [0, 0, 0, 0]

            >>> pattern.get_boolean_vector(8)
            [0, 0, 0, 0, 1, 1, 1, 1]

            >>> pattern.get_boolean_vector(16)
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

            Sets total length to length of pattern when ``total_length`` is
            none:

            >>> pattern.get_boolean_vector()
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ..  container:: example

            Gets vector of inverted pattern:

            >>> pattern = abjad.Pattern(
            ...     indices=[4, 5, 6, 7],
            ...     period=20,
            ... )

            >>> pattern.get_boolean_vector(4)
            [0, 0, 0, 0]

            >>> pattern.get_boolean_vector(8)
            [0, 0, 0, 0, 1, 1, 1, 1]

            >>> pattern.get_boolean_vector(16)
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

            Sets total length to length of pattern when ``total_length`` is
            none:

            >>> pattern.get_boolean_vector()
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ..  container:: example

            Two-part pattern with logical OR:

            >>> pattern = abjad.Pattern(
            ...     operator='or',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         abjad.Pattern(
            ...             indices=[-3, -2, -1],
            ...             ),
            ...         ],
            ... )

            >>> pattern.get_boolean_vector(4)
            [1, 1, 1, 1]

            >>> pattern.get_boolean_vector(8)
            [1, 1, 1, 0, 0, 1, 1, 1]

            >>> pattern.get_boolean_vector(16)
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

            Matches every index that is (one of the first three indices) OR
            (one of the last three indices).

        ..  container:: example

            Two-part pattern with mixed periodic and inverted parts:

            >>> pattern = abjad.Pattern(
            ...     operator='and',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0],
            ...             period=2,
            ...             ),
            ...         abjad.Pattern(
            ...             indices=[-3, -2, -1],
            ...             inverted=True,
            ...             ),
            ...         ],
            ... )

            >>> pattern.get_boolean_vector(4)
            [1, 0, 0, 0]

            >>> pattern.get_boolean_vector(8)
            [1, 0, 1, 0, 1, 0, 0, 0]

            >>> pattern.get_boolean_vector(16)
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]

            Matches every index that is (equal to 0 % 2) AND (not one of the
            last three indices).

        ..  container:: example

            Cyclic pattern that indexes every fourth and fifth item:

            >>> pattern_1 = abjad.Pattern([0], period=4)
            >>> pattern_2 = abjad.Pattern([0], period=5)
            >>> pattern = pattern_1 | pattern_2
            >>> pattern
            Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=4), Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=5)), payload=None, period=20)

            >>> pattern.get_boolean_vector(4)
            [1, 0, 0, 0]

            >>> pattern.get_boolean_vector(8)
            [1, 0, 0, 0, 1, 1, 0, 0]

            >>> pattern.get_boolean_vector(16)
            [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1]

            Sets total length to period of pattern when ``total_length`` is
            none:

            >>> pattern.period
            20

            >>> pattern.get_boolean_vector()
            [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0]

            >>> pattern.period == len(pattern.get_boolean_vector())
            True

        Returns list of ones and zeroes.
        """
        total_length = total_length or len(self)
        boolean_vector = []
        for index in range(total_length):
            result = self.matches_index(index, total_length)
            boolean_vector.append(int(result))
        return boolean_vector

    def get_matching_items(self, sequence):
        """
        Gets maching items from sequence.

        ..  container:: example

            >>> pattern = abjad.Pattern(
            ...     indices=[4, 5, 6, 7],
            ... )

            >>> pattern.get_matching_items('abcdefghijklmnopqrstuvwxyz')
            ['e', 'f', 'g', 'h']

        ..  container:: example

            >>> pattern = abjad.Pattern(
            ...     indices=[8, 9],
            ...     period=10,
            ... )

            >>> pattern.get_matching_items('abcdefghijklmnopqrstuvwxyz')
            ['i', 'j', 's', 't']

        ..  container:: example

            >>> pattern = abjad.index_first(1) | abjad.index_last(2)

            >>> pattern.get_matching_items('abcdefghijklmnopqrstuvwxyz')
            ['a', 'y', 'z']

        Returns list.
        """
        assert isinstance(sequence, collections.abc.Iterable), repr(sequence)
        length = len(sequence)
        items = []
        for i in range(length):
            if self.matches_index(i, length):
                item = sequence[i]
                items.append(item)
        return items

    @staticmethod
    def index(indices, period=None, inverted=None):
        """
        Makes pattern that matches ``indices``.

        ..  container:: example

            Indexes item 2:

            >>> pattern = abjad.index([2])
            >>> pattern
            Pattern(indices=(2,), inverted=None, operator=None, patterns=None, payload=None, period=None)

        ..  container:: example

            Indexes items 2, 3 and 5:

            >>> pattern = abjad.index([2, 3, 5])
            >>> pattern
            Pattern(indices=(2, 3, 5), inverted=None, operator=None, patterns=None, payload=None, period=None)

        Returns pattern.
        """
        assert all(isinstance(_, int) for _ in indices), repr(indices)
        indices = indices or []
        return Pattern(
            indices=indices,
            inverted=inverted,
            period=period,
        )

    @staticmethod
    def index_all(inverted=None):
        """
        Makes pattern that matches all indices.

        ..  container:: example

            Indexes all divisions for tie creation:

            >>> pattern = abjad.index_all()
            >>> pattern
            Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=1)

        Returns pattern.
        """
        return Pattern(indices=[0], inverted=inverted, period=1)

    @staticmethod
    def index_first(n, inverted=None):
        """
        Makes pattern that matches the first ``n`` indices.

        ..  container:: example

            Indexes first item:

            >>> pattern = abjad.index_first(1)
            >>> pattern
            Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=None)

        ..  container:: example

            Indexes first two items:

            >>> pattern = abjad.index_first(2)
            >>> pattern
            Pattern(indices=(0, 1), inverted=None, operator=None, patterns=None, payload=None, period=None)

        ..  container:: example

            Indexes nothing:

            >>> pattern = abjad.index_first(0)
            >>> pattern
            Pattern(indices=None, inverted=None, operator=None, patterns=None, payload=None, period=None)

        Returns pattern.
        """
        assert isinstance(n, int), repr(n)
        if 0 < n:
            indices = list(range(n))
        else:
            indices = None
        return Pattern(indices=indices, inverted=inverted)

    @staticmethod
    def index_last(n, inverted=None):
        """
        Makes pattern that matches the last ``n`` indices.

        ..  container:: example

            Indexes last two items:

            >>> pattern = abjad.index_last(2)
            >>> pattern
            Pattern(indices=(-2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)

        ..  container:: example

            Indexes nothing:

            >>> pattern = abjad.index_last(0)
            >>> pattern
            Pattern(indices=None, inverted=None, operator=None, patterns=None, payload=None, period=None)

        Returns pattern.
        """
        assert isinstance(n, int), repr(n)
        if 0 < n:
            start = -1
            stop = -n - 1
            stride = -1
            indices = list(reversed(range(start, stop, stride)))
        else:
            indices = None
        return Pattern(indices=indices, inverted=inverted)

    def matches_index(self, index, total_length, rotation=None):
        """
        Is true when pattern matches ``index`` taken under ``total_length``.

        ..  container:: example

            Matches three indices out of every eight:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ... )

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2
            3
            4
            5
            6
            7 True
            8 True
            9 True
            10
            11
            12
            13
            14
            15 True

            Matches three indices out of every eight, offset ``1`` to the left:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ... )

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(
            ...         index,
            ...         total_length,
            ...         rotation=1,
            ...         )
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1
            2
            3
            4
            5
            6 True
            7 True
            8 True
            9
            10
            11
            12
            13
            14 True
            15 True

            Matches three indices out of every eight, offset ``2`` to the
            left:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ... )

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(
            ...         index,
            ...         total_length,
            ...         rotation=2,
            ...         )
            ...     match = match or ''
            ...     print(index, match)
            0
            1
            2
            3
            4
            5 True
            6 True
            7 True
            8
            9
            10
            11
            12
            13 True
            14 True
            15 True

        ..  container:: example

            Matches three indices out of every sixteen:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=16,
            ... )

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2
            3
            4
            5
            6
            7 True
            8
            9
            10
            11
            12
            13
            14
            15

            Matches three indices out of every sixteen, offset ``1`` to the
            left:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=16,
            ... )

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(
            ...         index,
            ...         total_length,
            ...         rotation=1,
            ...         )
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1
            2
            3
            4
            5
            6 True
            7
            8
            9
            10
            11
            12
            13
            14
            15 True

            Matches three indices out of every sixteen, offset ``2`` to the
            left:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=16,
            ... )

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(
            ...         index,
            ...         total_length,
            ...         rotation=2,
            ...         )
            ...     match = match or ''
            ...     print(index, match)
            0
            1
            2
            3
            4
            5 True
            6
            7
            8
            9
            10
            11
            12
            13
            14 True
            15 True

        ..  container:: example

            Empty pattern:

            >>> pattern = abjad.Pattern()

            Total length 16:

            >>> total_length = 16
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0
            1
            2
            3
            4
            5
            6
            7
            8
            9
            10
            11
            12
            13
            14
            15

            Total length 8:

            >>> total_length = 8
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0
            1
            2
            3
            4
            5
            6
            7

            Total length 4:

            >>> total_length = 4
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0
            1
            2
            3

            Matches nothing.

        ..  container:: example

            Simple pattern:

            Logical OR:

            >>> pattern = abjad.Pattern(
            ...     operator='or',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         ],
            ... )
            >>> total_length = 16
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3
            4
            5
            6
            7
            8
            9
            10
            11
            12
            13
            14
            15

            Logical AND:

            >>> pattern = abjad.Pattern(
            ...     operator='and',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         ],
            ... )
            >>> total_length = 16
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3
            4
            5
            6
            7
            8
            9
            10
            11
            12
            13
            14
            15

            Logical XOR:

            >>> pattern = abjad.Pattern(
            ...     operator='xor',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         ],
            ... )
            >>> total_length = 16
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3
            4
            5
            6
            7
            8
            9
            10
            11
            12
            13
            14
            15

            Matches every index that is (one of the first three indices).

            Ignores ``operator``.

        ..  container:: example

            Two-part pattern with logical OR:

            >>> pattern = abjad.Pattern(
            ...     operator='or',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         abjad.Pattern(
            ...             indices=[-3, -2, -1],
            ...             ),
            ...         ],
            ... )

            Total length 16:

            >>> total_length = 16
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3
            4
            5
            6
            7
            8
            9
            10
            11
            12
            13 True
            14 True
            15 True

            Total length 8:

            >>> total_length = 8
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3
            4
            5 True
            6 True
            7 True

            Total length 4:

            >>> total_length = 4
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3 True

            Matches every index that is (one of the first three indices) OR
            (one of the last three indices).

        ..  container:: example

            Two-part pattern with logical AND:

            >>> pattern = abjad.Pattern(
            ...     operator='and',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         abjad.Pattern(
            ...             indices=[-3, -2, -1],
            ...             ),
            ...         ],
            ... )

            Total length 16:

            >>> total_length = 16
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0
            1
            2
            3
            4
            5
            6
            7
            8
            9
            10
            11
            12
            13
            14
            15

            Total length 8:

            >>> total_length = 8
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0
            1
            2
            3
            4
            5
            6
            7

            Total length 4:

            >>> total_length = 4
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0
            1 True
            2 True
            3

            Matches every index that is (one of the first three indices) AND
            (one of the last three indices).

        ..  container:: example

            Two-part pattern with logical XOR:

            >>> pattern = abjad.Pattern(
            ...     operator='xor',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         abjad.Pattern(
            ...             indices=[-3, -2, -1],
            ...             ),
            ...         ],
            ... )

            Total length 16:

            >>> total_length = 16
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3
            4
            5
            6
            7
            8
            9
            10
            11
            12
            13 True
            14 True
            15 True

            Total length 8:

            >>> total_length = 8
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3
            4
            5 True
            6 True
            7 True

            Total length 4:

            >>> total_length = 4
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1
            2
            3 True

            Matches every index that is (one of the first three indices) XOR
            (one of the last three indices).

        ..  container:: example

            Two-part pattern with mixed periodic and inverted parts:

            >>> pattern = abjad.Pattern(
            ...     operator='and',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0],
            ...             period=2,
            ...             ),
            ...         abjad.Pattern(
            ...             indices=[-3, -2, -1],
            ...             inverted=True,
            ...             ),
            ...         ],
            ... )

            Total length 16:

            >>> total_length = 16
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1
            2 True
            3
            4 True
            5
            6 True
            7
            8 True
            9
            10 True
            11
            12 True
            13
            14
            15

            Total length 8:

            >>> total_length = 8
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1
            2 True
            3
            4 True
            5
            6
            7

            Total length 4:

            >>> total_length = 4
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1
            2
            3

            Matches every index that is (equal to 0 % 2) AND (not one of the
            last three indices).

        ..  container:: example

            Complex pattern with compound and simple parts:

            >>> pattern = abjad.Pattern(
            ...     operator='and',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0],
            ...             period=2,
            ...             ),
            ...         abjad.Pattern(
            ...             indices=[-3, -2, -1],
            ...             inverted=True,
            ...             ),
            ...         ],
            ... )
            >>> pattern = abjad.Pattern(
            ...     operator='or',
            ...     patterns=[
            ...         pattern,
            ...         abjad.Pattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         ],
            ... )
            >>> pattern
            Pattern(indices=None, inverted=None, operator='or', patterns=(Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=2), Pattern(indices=(-3, -2, -1), inverted=True, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None), Pattern(indices=(0, 1, 2), inverted=None, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

            Total length 16:

            >>> total_length = 16
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3
            4 True
            5
            6 True
            7
            8 True
            9
            10 True
            11
            12 True
            13
            14
            15

            Total length 8:

            >>> total_length = 8
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3
            4 True
            5
            6
            7

            Total length 4:

            >>> total_length = 4
            >>> for index in range(total_length):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2 True
            3

            Matches every index that is ((equal to 0 % 2) AND (not one of the
            last three indices)) OR is (one of the first three indices).

        Returns true or false.
        """
        if not self.patterns:
            assert 0 <= total_length
            if 0 <= index:
                nonnegative_index = index
            else:
                nonnegative_index = total_length - abs(index)
            inverted = bool(self.inverted)
            if not self.indices:
                return False ^ inverted
            if self.period is None:
                for index in self.indices:
                    if index < 0:
                        index = total_length - abs(index)
                    if index == nonnegative_index and index < total_length:
                        return True ^ inverted
            else:
                if rotation is not None:
                    nonnegative_index += rotation
                nonnegative_index = nonnegative_index % self.period
                for index in self.indices:
                    if index < 0:
                        index = total_length - abs(index)
                        index = index % self.period
                    if index == nonnegative_index and index < total_length:
                        return True ^ inverted
                    if (index % self.period) == nonnegative_index and (
                        index % self.period < total_length
                    ):
                        return True ^ inverted
            return False ^ inverted
        elif len(self.patterns) == 1:
            pattern = self.patterns[0]
            result = pattern.matches_index(index, total_length, rotation=rotation)
        else:
            operator_ = self._name_to_operator[self.operator]
            pattern = self.patterns[0]
            result = pattern.matches_index(index, total_length, rotation=rotation)
            for pattern in self.patterns[1:]:
                result_ = pattern.matches_index(index, total_length, rotation=rotation)
                result = operator_(result, result_)
        if self.inverted:
            result = not (result)
        return result

    def reverse(self):
        """
        Reverses pattern.

        ..  container:: example

            Matches three indices out of every eight:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ... )

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2
            3
            4
            5
            6
            7 True
            8 True
            9 True
            10
            11
            12
            13
            14
            15 True

        ..  container:: example

            Reverses pattern:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ... )

            >>> pattern = pattern.reverse()
            >>> pattern
            Pattern(indices=(-1, -2, -8), inverted=None, operator=None, patterns=None, payload=None, period=8)

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1
            2
            3
            4
            5
            6 True
            7 True
            8 True
            9
            10
            11
            12
            13
            14 True
            15 True

        ..  container:: example

            Matches every index that is (equal to 0 % 2) AND (not one of the
            last three indices):

            >>> pattern = abjad.Pattern(
            ...     operator='and',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0],
            ...             period=2,
            ...             ),
            ...         abjad.Pattern(
            ...             indices=[-3, -2, -1],
            ...             inverted=True,
            ...             ),
            ...         ],
            ... )
            >>> pattern
            Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=2), Pattern(indices=(-3, -2, -1), inverted=True, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

            Reverses pattern:

            >>> pattern = pattern.reverse()
            >>> pattern
            Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(-1,), inverted=None, operator=None, patterns=None, payload=None, period=2), Pattern(indices=(2, 1, 0), inverted=True, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

            New pattern matches every index that is (equal to -1 % 2) AND (not one of the
            first three indices).

        Returns new pattern.
        """
        if not self.patterns:
            indices = [-index - 1 for index in self.indices]
            return dataclasses.replace(self, indices=indices)
        patterns = [_.reverse() for _ in self.patterns]
        return dataclasses.replace(self, patterns=patterns)

    def rotate(self, n=0):
        """
        Rotates pattern by index ``n``.

        ..  container:: example

            Matches three indices out of every eight:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ... )

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2
            3
            4
            5
            6
            7 True
            8 True
            9 True
            10
            11
            12
            13
            14
            15 True

            Rotates pattern two elements to the right:

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ... )

            >>> pattern = pattern.rotate(n=2)
            >>> pattern
            Pattern(indices=(2, 3, 9), inverted=None, operator=None, patterns=None, payload=None, period=8)

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0
            1 True
            2 True
            3 True
            4
            5
            6
            7
            8
            9 True
            10 True
            11 True
            12
            13
            14
            15

        ..  container:: example

            Matches three indices out of every eight with negative indices:

            >>> pattern = abjad.Pattern(
            ...     indices=[-3, -2, -1],
            ...     period=8,
            ... )

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0
            1
            2
            3
            4
            5 True
            6 True
            7 True
            8
            9
            10
            11
            12
            13 True
            14 True
            15 True

            Rotates pattern two elements to the right:

            >>> pattern = abjad.Pattern(
            ...     indices=[-3, -2, -1],
            ...     period=8,
            ... )

            >>> pattern = pattern.rotate(n=2)
            >>> pattern
            Pattern(indices=(-1, 0, 1), inverted=None, operator=None, patterns=None, payload=None, period=8)

            >>> total_length = 16
            >>> for index in range(16):
            ...     match = pattern.matches_index(index, total_length)
            ...     match = match or ''
            ...     print(index, match)
            0 True
            1 True
            2
            3
            4
            5
            6
            7 True
            8 True
            9 True
            10
            11
            12
            13
            14
            15 True

        ..  container:: example

            Matches every index that is (equal to 0 % 2) AND (not one of the
            last three indices):

            >>> pattern = abjad.Pattern(
            ...     operator='and',
            ...     patterns=[
            ...         abjad.Pattern(
            ...             indices=[0],
            ...             period=2,
            ...             ),
            ...         abjad.Pattern(
            ...             indices=[-3, -2, -1],
            ...             inverted=True,
            ...             ),
            ...         ],
            ... )
            >>> pattern
            Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(0,), inverted=None, operator=None, patterns=None, payload=None, period=2), Pattern(indices=(-3, -2, -1), inverted=True, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

            Rotates pattern two elements to the right:

            >>> pattern = pattern.rotate(n=2)
            >>> pattern
            Pattern(indices=None, inverted=None, operator='and', patterns=(Pattern(indices=(2,), inverted=None, operator=None, patterns=None, payload=None, period=2), Pattern(indices=(-1, 0, 1), inverted=True, operator=None, patterns=None, payload=None, period=None)), payload=None, period=None)

            New pattern matches every index that is (equal to 2 % 2) AND (not the first,
            second or last index in the pattern).

        Returns new pattern.
        """
        if not self.patterns:
            indices = [index + n for index in self.indices]
            return dataclasses.replace(self, indices=indices)
        patterns = [_.rotate(n=n) for _ in self.patterns]
        return dataclasses.replace(self, patterns=patterns)


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class PatternTuple:
    """
    Pattern tuple.

    ..  container:: example

        Three patterns:

        >>> patterns = abjad.PatternTuple([
        ...     abjad.Pattern(
        ...         indices=[0, 1, 7],
        ...         period=10,
        ...         ),
        ...     abjad.Pattern(
        ...         indices=[-2, -1],
        ...         ),
        ...     abjad.Pattern(
        ...         indices=[2],
        ...         period=3,
        ...         ),
        ...     ])
        >>> patterns
        PatternTuple(items=(Pattern(indices=(0, 1, 7), inverted=None, operator=None, patterns=None, payload=None, period=10), Pattern(indices=(-2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None), Pattern(indices=(2,), inverted=None, operator=None, patterns=None, payload=None, period=3)))

    ..  container:: example

        Two patterns:

        >>> patterns = abjad.PatternTuple([
        ...     abjad.Pattern(
        ...         indices=[1],
        ...         period=2,
        ...         ),
        ...     abjad.Pattern(
        ...         indices=[-3, -2, -1],
        ...         ),
        ...     ])
        >>> patterns
        PatternTuple(items=(Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2), Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)))

    """

    items: typing.Sequence = ()

    def __post_init__(self):
        self.items = tuple(self.items or [])

    def get_matching_pattern(self, index, total_length, rotation=None):
        """
        Gets pattern matching ``index``.

        ..  container:: example

            Two patterns:

            >>> patterns = abjad.PatternTuple([
            ...     abjad.Pattern(
            ...         indices=[1],
            ...         period=2,
            ...         ),
            ...     abjad.Pattern(
            ...         indices=[-3, -2, -1],
            ...         ),
            ...     ])

            Gets patterns that match the first ten indices:

            >>> for i in range(10):
            ...     match = patterns.get_matching_pattern(i, 10)
            ...     print(i, match)
            ...
            0 None
            1 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            2 None
            3 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            4 None
            5 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            6 None
            7 Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)
            8 Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)
            9 Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)

            Last three indices match the second pattern.

            Gets patterns that match next ten indices:

            >>> for i in range(10, 20):
            ...     match = patterns.get_matching_pattern(i, 10)
            ...     print(i, match)
            ...
            10 None
            11 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            12 None
            13 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            14 None
            15 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            16 None
            17 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            18 None
            19 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)

            Last three indices no longer match the second pattern.

        ..  container:: example

            Gets patterns that match the first ten indices, with rotation set
            to ``1``:

            >>> for i in range(10):
            ...     match = patterns.get_matching_pattern(i, 10, rotation=1)
            ...     print(i, match)
            ...
            0 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            1 None
            2 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            3 None
            4 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            5 None
            6 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            7 Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)
            8 Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)
            9 Pattern(indices=(-3, -2, -1), inverted=None, operator=None, patterns=None, payload=None, period=None)

            Matching indices of first pattern offset by ``1``.

            Gets patterns that match next ten indices with rotation set to
            ``1``:

            >>> for i in range(10, 20):
            ...     match = patterns.get_matching_pattern(i, 10, rotation=1)
            ...     print(i, match)
            ...
            10 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            11 None
            12 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            13 None
            14 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            15 None
            16 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            17 None
            18 Pattern(indices=(1,), inverted=None, operator=None, patterns=None, payload=None, period=2)
            19 None

            Matching indices of first pattern offset by ``1``.

        ..  container:: example

            With inverted patterns:

            >>> patterns = abjad.PatternTuple([
            ...     abjad.Pattern(
            ...         indices=[-3],
            ...         inverted=True,
            ...         ),
            ...     ])

            >>> for i in range(10):
            ...     match = patterns.get_matching_pattern(i, 10)
            ...     print(i, match)
            ...
            0 Pattern(indices=(-3,), inverted=True, operator=None, patterns=None, payload=None, period=None)
            1 Pattern(indices=(-3,), inverted=True, operator=None, patterns=None, payload=None, period=None)
            2 Pattern(indices=(-3,), inverted=True, operator=None, patterns=None, payload=None, period=None)
            3 Pattern(indices=(-3,), inverted=True, operator=None, patterns=None, payload=None, period=None)
            4 Pattern(indices=(-3,), inverted=True, operator=None, patterns=None, payload=None, period=None)
            5 Pattern(indices=(-3,), inverted=True, operator=None, patterns=None, payload=None, period=None)
            6 Pattern(indices=(-3,), inverted=True, operator=None, patterns=None, payload=None, period=None)
            7 None
            8 Pattern(indices=(-3,), inverted=True, operator=None, patterns=None, payload=None, period=None)
            9 Pattern(indices=(-3,), inverted=True, operator=None, patterns=None, payload=None, period=None)

        Returns pattern or none.
        """
        for pattern in reversed(self.items):
            if hasattr(pattern, "pattern"):
                if pattern.pattern.matches_index(
                    index, total_length, rotation=rotation
                ):
                    return pattern
            elif pattern.matches_index(index, total_length, rotation=rotation):
                return pattern

    def get_matching_payload(self, index, total_length, rotation=None):
        """
        Gets payload attached to pattern matching ``index``.

        ..  container:: example

            Two patterns. Underlying notes with even divisions
            assigned to the last three indices:

            >>> patterns = abjad.PatternTuple([
            ...     abjad.Pattern(
            ...         indices=[0],
            ...         payload='staccato',
            ...         period=1,
            ...         ),
            ...     abjad.Pattern(
            ...         indices=[-3, -2, -1],
            ...         payload='tenuto',
            ...         ),
            ...     ])

            Over ten indices:

            >>> for i in range(10):
            ...     match = patterns.get_matching_payload(i, 10)
            ...     print(i, match)
            ...
            0 staccato
            1 staccato
            2 staccato
            3 staccato
            4 staccato
            5 staccato
            6 staccato
            7 tenuto
            8 tenuto
            9 tenuto

            Over fifteen indices:

            >>> for i in range(15):
            ...     match = patterns.get_matching_payload(i, 15)
            ...     print(i, match)
            ...
            0 staccato
            1 staccato
            2 staccato
            3 staccato
            4 staccato
            5 staccato
            6 staccato
            7 staccato
            8 staccato
            9 staccato
            10 staccato
            11 staccato
            12 tenuto
            13 tenuto
            14 tenuto

        """
        pattern = self.get_matching_pattern(index, total_length, rotation=rotation)
        payload = None
        if pattern:
            payload = pattern.payload
        return payload
