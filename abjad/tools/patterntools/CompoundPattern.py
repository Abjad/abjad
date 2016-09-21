# -*- coding: utf-8 -*-
import operator
from abjad.tools import mathtools
from abjad.tools.topleveltools.new import new
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class CompoundPattern(TypedTuple):
    r'''Compound pattern.

    ..  container:: example

        **Example 1.** Matches every index that is (one of the first three
        indices) OR (one of the last three indices):

        ::

            >>> pattern = patterntools.CompoundPattern(
            ...     [
            ...         patterntools.Pattern(
            ...             indices=[0, 1, 2],
            ...             ),
            ...         patterntools.Pattern(
            ...             indices=[-3, -2, -1],
            ...             ),
            ...         ],
            ...     )

        ::

            >>> print(format(pattern))
            patterntools.CompoundPattern(
                (
                    patterntools.Pattern(
                        indices=(0, 1, 2),
                        ),
                    patterntools.Pattern(
                        indices=(-3, -2, -1),
                        ),
                    ),
                operator='or',
                )

        ..  container:: example

            **Example 2.** Matches every index that is (equal to 0 % 2) AND
            (not one of the last three indices):

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             inverted=True,
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0,),
                            period=2,
                            ),
                        patterntools.Pattern(
                            indices=(-3, -2, -1),
                            inverted=True,
                            ),
                        ),
                    operator='and',
                    )

        ..  container:: example

            **Example 3.** Sieve from opening of Xenakis's **Psappha**:

            ::

                >>> sieve_1a = patterntools.select_every([0, 1, 7], period=8)
                >>> sieve_1b = patterntools.select_every([1, 3], period=5)
                >>> sieve_1 = sieve_1a & sieve_1b
                >>> sieve_2a = patterntools.select_every([0, 1, 2], period=8)
                >>> sieve_2b = patterntools.select_every([0], period=5)
                >>> sieve_2 = sieve_2a & sieve_2b
                >>> sieve_3 = patterntools.select_every([3], period=8)
                >>> sieve_4 = patterntools.select_every([4], period=8)
                >>> sieve_5a = patterntools.select_every([5, 6], period=8)
                >>> sieve_5b = patterntools.select_every([2, 3, 4], period=5)
                >>> sieve_5 = sieve_5a & sieve_5b
                >>> sieve_6a = patterntools.select_every([1], period=8)
                >>> sieve_6b = patterntools.select_every([2], period=5)
                >>> sieve_6 = sieve_6a & sieve_6b
                >>> sieve_7a = patterntools.select_every([6], period=8)
                >>> sieve_7b = patterntools.select_every([1], period=5)
                >>> sieve_7 = sieve_7a & sieve_7b
                >>> sieve = sieve_1 | sieve_2 | sieve_3 | sieve_4 | sieve_5 | sieve_6 | sieve_7

            ::

                >>> sieve.get_boolean_vector(total_length=40)
                [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
                1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_inverted',
        '_operator',
        )

    _name_to_operator = {
        'and': operator.and_,
        'or': operator.or_,
        'xor': operator.xor,
        }

    ### INITIALIZER ###

    def __init__(self, items=None, inverted=None, operator='or'):
        from abjad.tools import patterntools
        items = items or ()
        prototype = (patterntools.Pattern, type(self))
        for item in items:
            assert isinstance(item, prototype), repr(item)
        assert operator in self._name_to_operator, repr(operator)
        TypedTuple.__init__(
            self,
            items=items,
            )
        self._inverted = inverted
        self._operator = operator

    ### SPECIAL METHODS ###

    def __and__(self, pattern):
        r'''Logical AND of two patterns.

        ..  container:: example

            **Example 1.** Flat grouping:

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern_3 = patterntools.select_every([0], period=2)
                >>> pattern = pattern_1 & pattern_2 & pattern_3

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0, 1, 2),
                            ),
                        patterntools.Pattern(
                            indices=(-3, -2, -1),
                            ),
                        patterntools.Pattern(
                            indices=(0,),
                            period=2,
                            ),
                        ),
                    operator='and',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ..  container:: example

            **Example 2.** Nested grouping:

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern_3 = patterntools.select_every([0], period=2)
                >>> pattern = pattern_1 & pattern_2 | pattern_3

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.CompoundPattern(
                            (
                                patterntools.Pattern(
                                    indices=(0, 1, 2),
                                    ),
                                patterntools.Pattern(
                                    indices=(-3, -2, -1),
                                    ),
                                ),
                            operator='and',
                            ),
                        patterntools.Pattern(
                            indices=(0,),
                            period=2,
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

        Returns new compound pattern.
        '''
        if self._can_append_to_self(pattern, 'and'):
            patterns = self.items + [pattern]
            result = type(self)(patterns, operator='and')
        else:
            result = type(self)([self, pattern], operator='and')
        return result

    def __invert__(self):
        r'''Inverts pattern.

        ..  container:: example

            **Example 1.** Matches every index that is (one of the first three
            indices) or (one of the last three indices):

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0, 1, 2),
                            ),
                        patterntools.Pattern(
                            indices=(-3, -2, -1),
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

        ..  container:: example

            **Example 2.** Matches every index that is NOT (one of the first
            three indices) or (one of the last three indices):

            ::

                >>> pattern = ~pattern
                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0, 1, 2),
                            ),
                        patterntools.Pattern(
                            indices=(-3, -2, -1),
                            ),
                        ),
                    inverted=True,
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

        Returns new compound pattern.
        '''
        inverted = not self.inverted
        pattern = new(self, inverted=inverted)
        return pattern

    def __or__(self, pattern):
        r'''Logical OR of two patterns.

        ..  container:: example

            **Example 1.** Flat grouping:

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern_3 = patterntools.select_every([0], period=2)
                >>> pattern = pattern_1 | pattern_2 | pattern_3

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0, 1, 2),
                            ),
                        patterntools.Pattern(
                            indices=(-3, -2, -1),
                            ),
                        patterntools.Pattern(
                            indices=(0,),
                            period=2,
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]

        ..  container:: example

            **Example 2.** Nested grouping:

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern_3 = patterntools.select_every([0], period=2)
                >>> pattern = pattern_1 | pattern_2 & pattern_3

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0, 1, 2),
                            ),
                        patterntools.CompoundPattern(
                            (
                                patterntools.Pattern(
                                    indices=(-3, -2, -1),
                                    ),
                                patterntools.Pattern(
                                    indices=(0,),
                                    period=2,
                                    ),
                                ),
                            operator='and',
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

        Returns new compound pattern.
        '''
        if self._can_append_to_self(pattern, 'or'):
            patterns = self.items + [pattern]
            result = type(self)(patterns, operator='or')
        else:
            result = type(self)([self, pattern], operator='or')
        return result

    def __xor__(self, pattern):
        r'''Logical XOR of two patterns.

        ..  container:: example

            **Example 1.** Flat grouping:

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern_3 = patterntools.select_every([0], period=2)
                >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0, 1, 2),
                            ),
                        patterntools.Pattern(
                            indices=(-3, -2, -1),
                            ),
                        patterntools.Pattern(
                            indices=(0,),
                            period=2,
                            ),
                        ),
                    operator='xor',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]

        ..  container:: example

            **Example 2.** Nested grouping:

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern_3 = patterntools.select_every([0], period=2)
                >>> pattern = pattern_1 ^ pattern_2 & pattern_3

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0, 1, 2),
                            ),
                        patterntools.CompoundPattern(
                            (
                                patterntools.Pattern(
                                    indices=(-3, -2, -1),
                                    ),
                                patterntools.Pattern(
                                    indices=(0,),
                                    period=2,
                                    ),
                                ),
                            operator='and',
                            ),
                        ),
                    operator='xor',
                    )

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

        Returns new compound pattern.
        '''
        if self._can_append_to_self(pattern, 'xor'):
            patterns = self.items + [pattern]
            result = type(self)(patterns, operator='xor')
        else:
            result = type(self)([self, pattern], operator='xor')
        return result

    ### PRIVATE METHODS ###

    def _can_append_to_self(self, pattern, operator_):
        from abjad.tools import patterntools
        if operator_ == self.operator:
            if isinstance(pattern, patterntools.Pattern):
                return True
            if (isinstance(pattern, type(self)) and
                pattern.operator == self.operator):
                return True
        return False

    ### PUBLIC METHODS ###

    def get_boolean_vector(self, total_length=None):
        r'''Gets boolean vector of pattern applied to input sequence with
        `total_length`.

        ..  container:: example

            **Example 1.** Two-part pattern with logical OR:

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             ),
                ...         ],
                ...     operator='or',
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

            **Example 2.** Two-part pattern with mixed periodic and inverted
            parts:

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             inverted=True,
                ...             ),
                ...         ],
                ...     operator='and',
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

            **Example 3.** Cyclic pattern that selects every fourth and fifth
            item:

            ::

                >>> pattern_1 = patterntools.Pattern([0], period=4)
                >>> pattern_2 = patterntools.Pattern([0], period=5)
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0,),
                            period=4,
                            ),
                        patterntools.Pattern(
                            indices=(0,),
                            period=5,
                            ),
                        ),
                    operator='or',
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
        total_length = total_length or self.period
        boolean_vector = []
        for index in range(total_length):
            result = self.matches_index(index, total_length)
            boolean_vector.append(int(result))
        return boolean_vector

    def matches_index(self, index, total_length, rotation=None):
        r'''Is true when compound pattern matches `index` under
        `total_length`. Otherwise false.

        ..  container:: example

            **Example 1.** Empty pattern:

            ::

                >>> pattern = patterntools.CompoundPattern()

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

            **Example 2.** Simple pattern:

            Logical OR:

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     operator='or',
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

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     operator='and',
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

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     operator='xor',
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

            **Example 3.** Two-part pattern with logical OR:

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             ),
                ...         ],
                ...     operator='or',
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

            **Example 4.** Two-part pattern with logical AND:

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             ),
                ...         ],
                ...     operator='and',
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

            **Example 5.** Two-part pattern with logical XOR:

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             ),
                ...         ],
                ...     operator='xor',
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

            **Example 6.** Two-part pattern with mixed periodic and inverted
            parts:

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             inverted=True,
                ...             ),
                ...         ],
                ...     operator='and',
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

            **Example 7.** Complex pattern with compound and simple parts:

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             inverted=True,
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )
                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         pattern,
                ...         patterntools.Pattern(
                ...             indices=[0, 1, 2],
                ...             ),
                ...         ],
                ...     operator='or',
                ...     )

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.CompoundPattern(
                            (
                                patterntools.Pattern(
                                    indices=(0,),
                                    period=2,
                                    ),
                                patterntools.Pattern(
                                    indices=(-3, -2, -1),
                                    inverted=True,
                                    ),
                                ),
                            operator='and',
                            ),
                        patterntools.Pattern(
                            indices=(0, 1, 2),
                            ),
                        ),
                    operator='or',
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
        if not self.items:
            result = False
        elif len(self.items) == 1:
            pattern = self.items[0]
            result = pattern.matches_index(
                index,
                total_length,
                rotation=rotation,
                )
        else:
            operator_ = self._name_to_operator[self.operator]
            pattern = self.items[0]
            result = pattern.matches_index(
                index,
                total_length,
                rotation=rotation,
                )
            for pattern in self.items[1:]:
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
        r'''Reverses compound pattern.

        ..  container:: example

            **Example 1.** Matches every index that is (equal to 0 % 2) AND
            (not one of the last three indices):

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             inverted=True,
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0,),
                            period=2,
                            ),
                        patterntools.Pattern(
                            indices=(-3, -2, -1),
                            inverted=True,
                            ),
                        ),
                    operator='and',
                    )

            Reverses pattern:

            ::

                >>> pattern = pattern.reverse()
                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(-1,),
                            period=2,
                            ),
                        patterntools.Pattern(
                            indices=(2, 1, 0),
                            inverted=True,
                            ),
                        ),
                    operator='and',
                    )

            New pattern matches every index that is (equal to -1 % 2) AND
            (not one of the first three indices).

        Returns new compound pattern.
        '''
        patterns = [_.reverse() for _ in self]
        return new(self, items=patterns)

    def rotate(self, n=0):
        r'''Rotates compound pattern.

        ..  container:: example

            **Example 1.** Matches every index that is (equal to 0 % 2) AND
            (not one of the last three indices):

            ::

                >>> pattern = patterntools.CompoundPattern(
                ...     [
                ...         patterntools.Pattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[-3, -2, -1],
                ...             inverted=True,
                ...             ),
                ...         ],
                ...     operator='and',
                ...     )

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0,),
                            period=2,
                            ),
                        patterntools.Pattern(
                            indices=(-3, -2, -1),
                            inverted=True,
                            ),
                        ),
                    operator='and',
                    )

            Rotates pattern two elements to the right:

            ::

                >>> pattern = pattern.rotate(n=2)
                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(2,),
                            period=2,
                            ),
                        patterntools.Pattern(
                            indices=(-1, 0, 1),
                            inverted=True,
                            ),
                        ),
                    operator='and',
                    )

            New pattern matches every index that is (equal to 2 % 2) AND (not
            the first, second or last index in the pattern).

        Returns new compound pattern.
        '''
        patterns = [_.rotate(n=n) for _ in self]
        return new(self, items=patterns)

    ### PUBLIC PROPERTIES ###

    @property
    def inverted(self):
        '''Is true when compound pattern is inverted. Otherwise false.

        ..  container:: example

            **Example 1.** Matches every index that is (one of the first three
            indices) OR (one of the last three indices):

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern = pattern_1 | pattern_2
                >>> pattern.inverted is None
                True

            ::

                >>> pattern.get_boolean_vector(total_length=16)
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]


        ..  container:: example

            **Example 2.** Matches every index that is NOT (one of the first
            three indices) OR (one of the last three indices):

            ::

                >>> pattern = new(pattern, inverted=True)
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
        r'''Gets operator of compounnd pattern.

        Set to string.

        Returns string.
        '''
        return self._operator

    @property
    def period(self):
        r'''Gets period of compound pattern.

        ..  container:: example

            **Example 1.** Gets period of pattern that selects every fourth and
            fifth element:

            ::

                >>> pattern_1 = patterntools.Pattern([0], period=4)
                >>> pattern_2 = patterntools.Pattern([0], period=5)
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0,),
                            period=4,
                            ),
                        patterntools.Pattern(
                            indices=(0,),
                            period=5,
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.period
                20

        ..  container:: example

            **Example 2.** Returns none when pattern contains acyclic parts:

            ::

                >>> pattern_1 = patterntools.Pattern([0], period=4)
                >>> pattern_2 = patterntools.Pattern([0])
                >>> pattern = pattern_1 | pattern_2

            ::

                >>> print(format(pattern))
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=(0,),
                            period=4,
                            ),
                        patterntools.Pattern(
                            indices=(0,),
                            ),
                        ),
                    operator='or',
                    )

            ::

                >>> pattern.period is None
                True

        Returns positive integer.
        '''
        periods = [_.period for _ in self]
        if None not in periods:
            return mathtools.least_common_multiple(*periods)
