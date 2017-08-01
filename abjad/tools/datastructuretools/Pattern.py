# -*- coding: utf-8 -*-
import collections
import operator
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class Pattern(AbjadValueObject):
    r'''Pattern.

    ::

        >>> import abjad
        >>> from abjad.tools import rhythmmakertools

    ..  container:: example

        Matches three indices out of every eight:

        ::

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=8,
            ...     )

        ::

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

        ::

            >>> pattern = abjad.Pattern(
            ...     indices=[0, 1, 7],
            ...     period=16,
            ...     )

        ::

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

        ::

            >>> pattern = abjad.Pattern(
            ...     indices=[16, 17, 23],
            ...     period=16,
            ...     )

        ::

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

        ::

            >>> sieve_1a = abjad.index_every([0, 1, 7], period=8)
            >>> sieve_1b = abjad.index_every([1, 3], period=5)
            >>> sieve_1 = sieve_1a & sieve_1b
            >>> sieve_2a = abjad.index_every([0, 1, 2], period=8)
            >>> sieve_2b = abjad.index_every([0], period=5)
            >>> sieve_2 = sieve_2a & sieve_2b
            >>> sieve_3 = abjad.index_every([3], period=8)
            >>> sieve_4 = abjad.index_every([4], period=8)
            >>> sieve_5a = abjad.index_every([5, 6], period=8)
            >>> sieve_5b = abjad.index_every([2, 3, 4], period=5)
            >>> sieve_5 = sieve_5a & sieve_5b
            >>> sieve_6a = abjad.index_every([1], period=8)
            >>> sieve_6b = abjad.index_every([2], period=5)
            >>> sieve_6 = sieve_6a & sieve_6b
            >>> sieve_7a = abjad.index_every([6], period=8)
            >>> sieve_7b = abjad.index_every([1], period=5)
            >>> sieve_7 = sieve_7a & sieve_7b
            >>> sieve = sieve_1 | sieve_2 | sieve_3 | sieve_4 | sieve_5 | sieve_6 | sieve_7

        ::

            >>> sieve.get_boolean_vector(total_length=40)
            [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
            1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_indices',
        '_inverted',
        '_operator',
        '_patterns',
        '_payload',
        '_period',
        )

    _name_to_operator = {
        'and': operator.and_,
        'or': operator.or_,
        'xor': operator.xor,
        }

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        indices=None,
        inverted=None,
        operator=None,
        patterns=None,
        payload=None,
        period=None,
        ):
        if indices is not None:
            assert all(isinstance(_, int) for _ in indices), repr(indices)
            indices = tuple(indices)
        self._indices = indices
        if inverted is not None:
            inverted = bool(inverted)
        self._inverted = inverted
        if operator is not None:
            assert operator in self._name_to_operator, repr(operator)
        self._operator = operator
        if period is not None:
            assert mathtools.is_positive_integer(period), repr(period)
        if patterns is not None:
            assert all(isinstance(_, type(self)) for _ in patterns)
            patterns = tuple(patterns)
        self._patterns = patterns
        self._payload = payload
        self._period = period

    ### SPECIAL METHODS ###

    def __and__(self, pattern):
        r'''Logical AND of two patterns.

        ..  container:: example

            Flat grouping of two patterns:

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern = pattern_1 & pattern_2

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='and',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        ),
                    )

        ..  container:: example

            Flat grouping of three patterns:

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern_3 = abjad.index_every([0], period=2)
                >>> pattern = pattern_1 & pattern_2 & pattern_3

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='and',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        abjad.Pattern(
                            indices=[0],
                            period=2,
                            ),
                        ),
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ..  container:: example

            Nested grouping of three patterns:

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern_3 = abjad.index_every([0], period=2)
                >>> pattern = pattern_1 & pattern_2 | pattern_3

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            operator='and',
                            patterns=(
                                abjad.Pattern(
                                    indices=[0, 1, 2],
                                    ),
                                abjad.Pattern(
                                    indices=[-3, -2, -1],
                                    ),
                                ),
                            ),
                        abjad.Pattern(
                            indices=[0],
                            period=2,
                            ),
                        ),
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

        ..  container:: example

            In-place AND is allowed:

            ::

                >>> pattern = abjad.index_first(3)
                >>> pattern &= abjad.index_last(3)

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='and',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        ),
                    )

        Returns new pattern.
        '''
        if self._can_append_to_self(pattern, 'and'):
            if self.patterns is None:
                self_patterns = [self]
            else:
                self_patterns = list(self.patterns)
            patterns = self_patterns + [pattern]
            result = type(self)(operator='and', patterns=patterns)
        else:
            result = type(self)(operator='and', patterns=[self, pattern])
        return result

    def __invert__(self):
        r'''Inverts pattern.

        ..  container:: example

            ::

                >>> pattern = abjad.index_first(3)
                >>> f(pattern)
                abjad.Pattern(
                    indices=[0, 1, 2],
                    )

            ::

                >>> pattern = ~pattern
                >>> f(pattern)
                abjad.Pattern(
                    indices=[0, 1, 2],
                    inverted=True,
                    )

            ::

                >>> pattern = ~pattern
                >>> f(pattern)
                abjad.Pattern(
                    indices=[0, 1, 2],
                    inverted=False,
                    )

            Negation defined equal to inversion.

        ..  container:: example

            Matches every index that is (one of the first three indices) or
            (one of the last three indices):

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        ),
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

        ..  container:: example

            Matches every index that is NOT (one of the first three indices) or
            (one of the last three indices):

            ::

                >>> pattern = ~pattern
                >>> f(pattern)
                abjad.Pattern(
                    inverted=True,
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        ),
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

        Returns new pattern.
        '''
        import abjad
        inverted = not self.inverted
        pattern = abjad.new(self, inverted=inverted)
        return pattern

    def __len__(self):
        r'''Gets length of pattern.

        ..  container:: example

            Gets length of cyclic pattern:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> len(pattern)
                8

            Length of cyclic pattern defined equal to period of the pattern.

        ..  container:: example

            Gets length of acyclic pattern:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 2, 3],
                ...     )

            ::

                >>> len(pattern)
                4

            Length of acyclic pattern defined equal to greatest index in
            pattern, plus 1.

        ..  container:: example

            Gets length of pattern with negative indices:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[-3],
                ...     )

            ::

                >>> len(pattern)
                3

            Length of pattern with negative indices defined equal to absolute
            value of least index.

        Returns nonnegative integer.
        '''
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
        r'''Logical OR of two patterns.

        ..  container:: example

            Flat grouping of two patterns:

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        ),
                    )

        ..  container:: example

            Flat grouping:

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern_3 = abjad.index_every([0], period=2)
                >>> pattern = pattern_1 | pattern_2 | pattern_3

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        abjad.Pattern(
                            indices=[0],
                            period=2,
                            ),
                        ),
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]

        ..  container:: example

            Nested grouping:

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern_3 = abjad.index_every([0], period=2)
                >>> pattern = pattern_1 | pattern_2 & pattern_3

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            operator='and',
                            patterns=(
                                abjad.Pattern(
                                    indices=[-3, -2, -1],
                                    ),
                                abjad.Pattern(
                                    indices=[0],
                                    period=2,
                                    ),
                                ),
                            ),
                        ),
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

        ..  container:: example

            In-place OR is allowed:

            ::

                >>> pattern = abjad.index_first(3)
                >>> pattern |= abjad.index_last(3)

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        ),
                    )

        Returns new pattern.
        '''
        if self._can_append_to_self(pattern, 'or'):
            if self.patterns is None:
                self_patterns = [self]
            else:
                self_patterns = list(self.patterns)
            patterns = self_patterns + [pattern]
            result = type(self)(operator='or', patterns=patterns)
        else:
            result = type(self)(operator='or', patterns=[self, pattern])
        return result

    def __xor__(self, pattern):
        r'''Logical XOR of two patterns.

        ..  container:: example

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern = pattern_1 ^ pattern_2

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='xor',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        ),
                    )

        ..  container:: example

            Flat grouping:

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern_3 = abjad.index_every([0], period=2)
                >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='xor',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        abjad.Pattern(
                            indices=[0],
                            period=2,
                            ),
                        ),
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]

        ..  container:: example

            Nested grouping:

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern_3 = abjad.index_every([0], period=2)
                >>> pattern = pattern_1 ^ pattern_2 & pattern_3

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='xor',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            operator='and',
                            patterns=(
                                abjad.Pattern(
                                    indices=[-3, -2, -1],
                                    ),
                                abjad.Pattern(
                                    indices=[0],
                                    period=2,
                                    ),
                                ),
                            ),
                        ),
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

        ..  container:: example

            In-place XOR is allowed:

            ::

                >>> pattern = abjad.index_first(3)
                >>> pattern ^= abjad.index_last(3)

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='xor',
                    patterns=(
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            ),
                        ),
                    )


        Returns new pattern.
        '''
        if self._can_append_to_self(pattern, 'xor'):
            if self.patterns is None:
                self_patterns = [self]
            else:
                self_patterns = list(self.patterns)
            patterns = self_patterns + [pattern]
            result = type(self)(operator='xor', patterns=patterns)
        else:
            result = type(self)(operator='xor', patterns=[self, pattern])
        return result

    ### PRIVATE METHODS ###

    def _can_append_to_self(self, pattern, operator_):
        if not isinstance(pattern, type(self)):
            return False
        if self.operator is None:
            return True
        if (self.operator == operator_ and
            (pattern.operator is None or
            (pattern.operator == self.operator))):
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def indices(self):
        r'''Gets indices of pattern.

        ..  container:: example

            Matches three indices out of every eight:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.indices
                [0, 1, 7]

        ..  container:: example

            Matches three indices out of every sixteen:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

                >>> pattern.indices
                [0, 1, 7]

        Defaults to none.

        Set to integers or none.

        Returns integers or none.
        '''
        if self._indices:
            return list(self._indices)

    @property
    def inverted(self):
        r'''Is true when pattern is inverted. Otherwise false.

        ..  container:: example

            Matches three indices out of every eight:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.inverted is None
                True

            ::

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

            Pattern that rejects three indices from every eight; equivalently,
            pattern matches ``8-3=5`` indices out of every eight:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     inverted=True
                ...     )

            ::

                >>> pattern.inverted
                True

            ::

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

        ..  container:: example

            Matches every index that is (one of the first three indices) OR
            (one of the last three indices):

            ::

                >>> pattern_1 = abjad.index_first(3)
                >>> pattern_2 = abjad.index_last(3)
                >>> pattern = pattern_1 | pattern_2
                >>> pattern.inverted is None
                True

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]


        ..  container:: example

            Matches every index that is NOT (one of the first three indices) OR
            (one of the last three indices):

            ::

                >>> pattern = abjad.new(pattern, inverted=True)
                >>> pattern.inverted
                True

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._inverted

    @property
    def operator(self):
        r'''Gets operator of pattern.

        Set to string.

        Returns string.
        '''
        return self._operator

    @property
    def patterns(self):
        r'''Gets paterns of pattern.

        Set to patterns or none.

        Returns tuple of patterns or none.
        '''
        return self._patterns

    @property
    def payload(self):
        r'''Gets payload of pattern.

        ..  container:: example

            Pattern with rhythm-maker payload assigned to three
            of every eight indices:

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     payload=maker,
                ...     period=8,
                ...     )

            ::

                >>> total_length = 10
                >>> for index in range(10):
                ...     match = pattern.matches_index(index, total_length)
                ...     if match:
                ...         payload = pattern.payload
                ...     else:
                ...         payload = ''
                ...     print(index, payload)
                0 NoteRhythmMaker()
                1 NoteRhythmMaker()
                2
                3
                4
                5
                6
                7 NoteRhythmMaker()
                8 NoteRhythmMaker()
                9 NoteRhythmMaker()

        Defaults to none.

        Set to any object.

        Returns arbitrary object.
        '''
        return self._payload

    @property
    def period(self):
        r'''Gets period of pattern.

        ..  container:: example

            Pattern with a period of eight:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.period
                8

            ::

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

            Same pattern with a period of sixteen:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

                >>> pattern.period
                16

            ::

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

            Gets period of pattern that indexs every fourth and fifth element:

            ::

                >>> pattern_1 = abjad.Pattern([0], period=4)
                >>> pattern_2 = abjad.Pattern([0], period=5)
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            indices=[0],
                            period=4,
                            ),
                        abjad.Pattern(
                            indices=[0],
                            period=5,
                            ),
                        ),
                    period=20,
                    )

            ::

                >>> pattern.period
                20

        ..  container:: example

            Returns none when pattern contains acyclic parts:

            ::

                >>> pattern_1 = abjad.Pattern([0], period=4)
                >>> pattern_2 = abjad.Pattern([0])
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            indices=[0],
                            period=4,
                            ),
                        abjad.Pattern(
                            indices=[0],
                            ),
                        ),
                    )

            ::

                >>> pattern.period is None
                True

        Defaults to none.

        Set to positive integer or none.

        Returns positive integer or none.
        '''
        if self._period is not None:
            return self._period
        if self.patterns:
            periods = [_.period for _ in self.patterns]
            if None not in periods:
                return mathtools.least_common_multiple(*periods)

    @property
    def weight(self):
        r'''Gets weight of pattern.

        ..  container:: example

            Gets weight of cyclic pattern:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.weight
                3

        ..  container:: example

            Gets weight of acyclic pattern:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 2, 3],
                ...     )

            ::

                >>> pattern.weight
                3

        Weight defined equal to number of indices in pattern.

        Returns nonnegative integer.
        '''
        return len(self.indices)

    ### PUBLIC METHODS ###

    @classmethod
    def from_vector(class_, vector):
        r'''Makes pattern from boolean `vector`.

        ..  container:: example

            Matches three indices out of every five:

            ::

                >>> pattern = [1, 0, 0, 1, 1]
                >>> pattern = abjad.Pattern.from_vector(pattern)
                >>> f(pattern)
                abjad.Pattern(
                    indices=[0, 3, 4],
                    period=5,
                    )

            ::

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

            ::

                >>> pattern = [1, 0, 0, 1, 1, 0]
                >>> pattern = abjad.Pattern.from_vector(pattern)
                >>> f(pattern)
                abjad.Pattern(
                    indices=[0, 3, 4],
                    period=6,
                    )

            ::

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
        '''
        vector = [bool(_) for _ in vector]
        period = len(vector)
        indices = [i for i, x in enumerate(vector) if x]
        return class_(
            period=period,
            indices=indices,
            )

    def get_boolean_vector(self, total_length=None):
        r'''Gets boolean vector of pattern applied to input sequence with
        `total_length`.

        ..  container:: example

            Gets boolean vector of acyclic pattern:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[4, 5, 6, 7],
                ...     )


            ::

                >>> pattern.get_boolean_vector(4)
                [0, 0, 0, 0]

            ::

                >>> pattern.get_boolean_vector(8)
                [0, 0, 0, 0, 1, 1, 1, 1]

            ::

                >>> pattern.get_boolean_vector(16)
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

            Sets total length to length of pattern when `total_length` is none:

            ::

                >>> pattern.get_boolean_vector()
                [0, 0, 0, 0, 1, 1, 1, 1]

        ..  container:: example

            Gets vector of cyclic pattern:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[4, 5, 6, 7],
                ...     period=20,
                ...     )

            ::

                >>> pattern.get_boolean_vector(4)
                [0, 0, 0, 0]

            ::

                >>> pattern.get_boolean_vector(8)
                [0, 0, 0, 0, 1, 1, 1, 1]

            ::

                >>> pattern.get_boolean_vector(16)
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

            Sets total length to length of pattern when `total_length` is none:

            ::

                >>> pattern.get_boolean_vector()
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ..  container:: example

            Gets vector of inverted pattern:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[4, 5, 6, 7],
                ...     period=20,
                ...     )

            ::

                >>> pattern.get_boolean_vector(4)
                [0, 0, 0, 0]

            ::

                >>> pattern.get_boolean_vector(8)
                [0, 0, 0, 0, 1, 1, 1, 1]

            ::

                >>> pattern.get_boolean_vector(16)
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

            Sets total length to length of pattern when `total_length` is none:

            ::

                >>> pattern.get_boolean_vector()
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ..  container:: example

            Two-part pattern with logical OR:

            ::

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
                ...     )

            ::

                >>> pattern.get_boolean_vector(4)
                [1, 1, 1, 1]

            ::

                >>> pattern.get_boolean_vector(8)
                [1, 1, 1, 0, 0, 1, 1, 1]


            ::

                >>> pattern.get_boolean_vector(16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

            Matches every index that is (one of the first three indices) OR
            (one of the last three indices).

        ..  container:: example

            Two-part pattern with mixed periodic and inverted parts:

            ::

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
                ...     )

            ::

                >>> pattern.get_boolean_vector(4)
                [1, 0, 0, 0]

            ::

                >>> pattern.get_boolean_vector(8)
                [1, 0, 1, 0, 1, 0, 0, 0]

            ::

                >>> pattern.get_boolean_vector(16)
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]

            Matches every index that is (equal to 0 % 2) AND (not one of the
            last three indices).

        ..  container:: example

            Cyclic pattern that indexes every fourth and fifth item:

            ::

                >>> pattern_1 = abjad.Pattern([0], period=4)
                >>> pattern_2 = abjad.Pattern([0], period=5)
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            indices=[0],
                            period=4,
                            ),
                        abjad.Pattern(
                            indices=[0],
                            period=5,
                            ),
                        ),
                    period=20,
                    )

            ::

                >>> pattern.get_boolean_vector(4)
                [1, 0, 0, 0]

            ::

                >>> pattern.get_boolean_vector(8)
                [1, 0, 0, 0, 1, 1, 0, 0]

            ::

                >>> pattern.get_boolean_vector(16)
                [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1]

            Sets total length to period of pattern when `total_length` is none:

            ::

                >>> pattern.period
                20

            ::

                >>> pattern.get_boolean_vector()
                [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0]

            ::

                >>> pattern.period == len(pattern.get_boolean_vector())
                True

        Returns list of ones and zeroes.
        '''
        total_length = total_length or len(self)
        boolean_vector = []
        for index in range(total_length):
            result = self.matches_index(index, total_length)
            boolean_vector.append(int(result))
        return boolean_vector

    def get_matching_items(self, sequence):
        r'''Gets maching items from sequence.

        ..  container:: example

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[4, 5, 6, 7],
                ...     )

            ::

                >>> pattern.get_matching_items('abcdefghijklmnopqrstuvwxyz')
                Sequence(['e', 'f', 'g', 'h'])

        ..  container:: example

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[8, 9],
                ...     period=10,
                ...     )

            ::

                >>> pattern.get_matching_items('abcdefghijklmnopqrstuvwxyz')
                Sequence(['i', 'j', 's', 't'])

        ..  container:: example

            ::

                >>> pattern = abjad.index_first(1) | abjad.index_last(2)

            ::

                >>> pattern.get_matching_items('abcdefghijklmnopqrstuvwxyz')
                Sequence(['a', 'y', 'z'])

        Returns new sequence.
        '''
        import abjad
        assert isinstance(sequence, collections.Iterable), repr(sequence)
        length = len(sequence)
        items = []
        for i in range(length):
            if self.matches_index(i, length):
                item = sequence[i]
                items.append(item)
        return abjad.Sequence(items=items)

    @staticmethod
    def index(indices=None, inverted=None):
        r'''Makes pattern that matches `indices`.

        ..  container:: example

            Indexes item 2:

            ::

                >>> pattern = abjad.index([2])

            ::

                >>> f(pattern)
                abjad.Pattern(
                    indices=[2],
                    )

        ..  container:: example

            Indexes items 2, 3 and 5:

            ::

                >>> pattern = abjad.index([2, 3, 5])

            ::

                >>> f(pattern)
                abjad.Pattern(
                    indices=[2, 3, 5],
                    )

        Returns pattern.
        '''
        indices = indices or []
        return Pattern(
            indices=indices,
            inverted=inverted,
            )

    @staticmethod
    def index_all(inverted=None):
        r'''Makes pattern that matches all indices.

        ..  container:: example

            Indexes all divisions for tie creation:

            ::

                >>> pattern = abjad.index_all()

            ::

                >>> f(pattern)
                abjad.Pattern(
                    indices=[0],
                    period=1,
                    )

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4. \repeatTie
                    }
                    {
                        \time 7/16
                        c'4.. \repeatTie
                    }
                    {
                        \time 3/8
                        c'4. \repeatTie
                    }
                }

        Returns pattern.
        '''
        return Pattern(
            indices=[0],
            inverted=inverted,
            period=1,
            )

    @staticmethod
    def index_every(indices, period=None, inverted=None):
        r'''Makes pattern that matches `indices` at `period`.

        ..  container:: example

            Indexes every second division:

            ::

                >>> mask = abjad.index_every(indices=[1], period=2)

            ::

                >>> print(format(mask))
                abjad.Pattern(
                    indices=[1],
                    period=2,
                    )

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        ..  container:: example

            Indexes every second and third division:

            ::

                >>> mask = abjad.index_every(indices=[1, 2], period=3)

            ::

                >>> print(format(mask))
                abjad.Pattern(
                    indices=[1, 2],
                    period=3,
                    )

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }


        Returns pattern.
        '''
        return Pattern(
            indices=indices,
            inverted=inverted,
            period=period,
            )

    @staticmethod
    def index_first(n=1, inverted=None):
        r'''Makes pattern that matches the first `n` indices.

        ..  container:: example

            Indexes first division for tie creation:

            ::

                >>> pattern = abjad.index_first()

            ::

                >>> f(pattern)
                abjad.Pattern(
                    indices=[0],
                    )

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4. \repeatTie
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }
                
        ..  container:: example

            Selects first two divisions for tie creation:

            ::

                >>> pattern = abjad.index_first(n=2)

            ::

                >>> f(pattern)
                abjad.Pattern(
                    indices=[0, 1],
                    )

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4. \repeatTie
                    }
                    {
                        \time 7/16
                        c'4.. \repeatTie
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            Selects no divisions for tie creation:

            ::

                >>> pattern = abjad.index_first(n=0)

            ::

                >>> f(pattern)
                abjad.Pattern()

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Returns pattern.
        '''
        if 0 < n:
            indices = list(range(n))
        else:
            indices = None
        return Pattern(
            indices=indices,
            inverted=inverted,
            )

    @staticmethod
    def index_last(n=1, inverted=None):
        r'''Makes pattern that matches the last `n` indices.

        ..  container:: example

            Indexes last two divisions for tie creation:

            ::

                >>> pattern = abjad.index_last(n=2)

            ::

                >>> f(pattern)
                abjad.Pattern(
                    indices=[-2, -1],
                    )

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4. \repeatTie
                    }
                }

            (Tie creation happens between adjacent divisions. Selecting only the
            last division creates no ties.)

        ..  container:: example

            Selects no divisions for tie creation:

            ::

                >>> pattern = abjad.index_last(n=0)

            ::

                >>> f(pattern)
                abjad.Pattern()

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Returns pattern.
        '''
        if 0 < n:
            indices = list(reversed(range(-1, -n-1, -1)))
        else:
            indices = None
        return Pattern(
            indices=indices,
            inverted=inverted,
            )

    def matches_index(self, index, total_length, rotation=None):
        r'''Is true when pattern matches `index` taken under `total_length`.
        Otherwise false.

        ..  container:: example

            Matches three indices out of every eight:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

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

            ::

                >>> pattern = abjad.Pattern()

            Total length 16:

            ::

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

            ::

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

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     operator='or',
                ...     patterns=[
                ...         abjad.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     )
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

            ::

                >>> pattern = abjad.Pattern(
                ...     operator='and',
                ...     patterns=[
                ...         abjad.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     )
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

            ::

                >>> pattern = abjad.Pattern(
                ...     operator='xor',
                ...     patterns=[
                ...         abjad.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     )
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

            Ignores `operator`.

        ..  container:: example

            Two-part pattern with logical OR:

            ::

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
                ...     )

            Total length 16:

            ::

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

            ::

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

            ::

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

            ::

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
                ...     )

            Total length 16:

            ::

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

            ::

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

            ::

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

            ::

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
                ...     )

            Total length 16:

            ::

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

            ::

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

            ::

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

            ::

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
                ...     )

            Total length 16:

            ::

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

            ::

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

            ::

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

            ::

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
                ...     )
                >>> pattern = abjad.Pattern(
                ...     operator='or',
                ...     patterns=[
                ...         pattern,
                ...         abjad.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     )

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='or',
                    patterns=(
                        abjad.Pattern(
                            operator='and',
                            patterns=(
                                abjad.Pattern(
                                    indices=[0],
                                    period=2,
                                    ),
                                abjad.Pattern(
                                    indices=[-3, -2, -1],
                                    inverted=True,
                                    ),
                                ),
                            ),
                        abjad.Pattern(
                            indices=[0, 1, 2],
                            ),
                        ),
                    )

            Total length 16:

            ::

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

            ::

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

            ::

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
        '''
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
                    if ((index % self.period) == nonnegative_index and
                        (index % self.period < total_length)):
                        return True ^ inverted
            return False ^ inverted
        elif len(self.patterns) == 1:
            pattern = self.patterns[0]
            result = pattern.matches_index(
                index,
                total_length,
                rotation=rotation,
                )
        else:
            operator_ = self._name_to_operator[self.operator]
            pattern = self.patterns[0]
            result = pattern.matches_index(
                index,
                total_length,
                rotation=rotation,
                )
            for pattern in self.patterns[1:]:
                result_ = pattern.matches_index(
                    index,
                    total_length,
                    rotation=rotation,
                    )
                result = operator_(result, result_)
        if self.inverted:
            result = not(result)
        return result

    def reverse(self):
        r'''Reverses pattern.

        ..  container:: example

            Matches three indices out of every eight:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern = pattern.reverse()
                >>> f(pattern)
                abjad.Pattern(
                    indices=[-1, -2, -8],
                    period=8,
                    )

            ::

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

            ::

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
                ...     )

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='and',
                    patterns=(
                        abjad.Pattern(
                            indices=[0],
                            period=2,
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            inverted=True,
                            ),
                        ),
                    )

            Reverses pattern:

            ::

                >>> pattern = pattern.reverse()
                >>> f(pattern)
                abjad.Pattern(
                    operator='and',
                    patterns=(
                        abjad.Pattern(
                            indices=[-1],
                            period=2,
                            ),
                        abjad.Pattern(
                            indices=[2, 1, 0],
                            inverted=True,
                            ),
                        ),
                    )

            New pattern matches every index that is (equal to -1 % 2) AND
            (not one of the first three indices).

        Returns new pattern.
        '''
        import abjad
        if not self.patterns:
            indices = [-index - 1 for index in self.indices]
            return abjad.new(self, indices=indices)
        patterns = [_.reverse() for _ in self.patterns]
        return abjad.new(self, patterns=patterns)

    def rotate(self, n=0):
        r'''Rotates pattern by index `n`.

        ..  container:: example

            Matches three indices out of every eight:

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern = pattern.rotate(n=2)
                >>> f(pattern)
                abjad.Pattern(
                    indices=[2, 3, 9],
                    period=8,
                    )

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[-3, -2, -1],
                ...     period=8,
                ...     )

            ::

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

            ::

                >>> pattern = abjad.Pattern(
                ...     indices=[-3, -2, -1],
                ...     period=8,
                ...     )

            ::

                >>> pattern = pattern.rotate(n=2)
                >>> f(pattern)
                abjad.Pattern(
                    indices=[-1, 0, 1],
                    period=8,
                    )

            ::

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

            ::

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
                ...     )

            ::

                >>> f(pattern)
                abjad.Pattern(
                    operator='and',
                    patterns=(
                        abjad.Pattern(
                            indices=[0],
                            period=2,
                            ),
                        abjad.Pattern(
                            indices=[-3, -2, -1],
                            inverted=True,
                            ),
                        ),
                    )

            Rotates pattern two elements to the right:

            ::

                >>> pattern = pattern.rotate(n=2)
                >>> f(pattern)
                abjad.Pattern(
                    operator='and',
                    patterns=(
                        abjad.Pattern(
                            indices=[2],
                            period=2,
                            ),
                        abjad.Pattern(
                            indices=[-1, 0, 1],
                            inverted=True,
                            ),
                        ),
                    )

            New pattern matches every index that is (equal to 2 % 2) AND (not
            the first, second or last index in the pattern).

        Returns new pattern.
        '''
        import abjad
        if not self.patterns:
            indices = [index + n for index in self.indices]
            return abjad.new(self, indices=indices)
        patterns = [_.rotate(n=n) for _ in self.patterns]
        return abjad.new(self, patterns=patterns)
