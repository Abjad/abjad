# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools.new import new


class Pattern(AbjadValueObject):
    r'''Pattern.

    ..  container:: example

        **Example 1.** Matches three indices out of every eight:

        ::

            >>> pattern = patterntools.Pattern(
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

        **Example 2.** Matches three indices out of every sixteen:

        ::

            >>> pattern = patterntools.Pattern(
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

        **Example 3.** Works with improper indices:

        ::

            >>> pattern = patterntools.Pattern(
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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_indices',
        '_inverted',
        '_payload',
        '_period',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        indices=None,
        inverted=None,
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
        if period is not None:
            assert mathtools.is_positive_integer(period), repr(period)
        self._payload = payload
        self._period = period

    ### SPECIAL METHODS ###

    def __and__(self, other):
        r'''Logical AND of two patterns.

        ..  container:: example

            **Example.**

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern = pattern_1 & pattern_2

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
                    operator='and',
                    )

        Returns compound pattern.
        '''
        from abjad.tools import patterntools
        return patterntools.CompoundPattern([self, other], operator='and')

    def __invert__(self):
        r'''Inverts pattern.

        ..  container:: example

            **Example.**

            ::

                >>> pattern = patterntools.select_first(3)
                >>> print(format(pattern))
                patterntools.Pattern(
                    indices=(0, 1, 2),
                    )

            ::

                >>> pattern = ~pattern
                >>> print(format(pattern))
                patterntools.Pattern(
                    indices=(0, 1, 2),
                    inverted=True,
                    )

            ::

                >>> pattern = ~pattern
                >>> print(format(pattern))
                patterntools.Pattern(
                    indices=(0, 1, 2),
                    inverted=False,
                    )

            Negation defined equal to inversion.

        Returns new pattern.
        '''
        inverted = not self.inverted
        pattern = new(self, inverted=inverted)
        return pattern

    def __len__(self):
        r'''Gets length of pattern.

        ..  container:: example

            **Example 1.** Gets length of cyclic pattern:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> len(pattern)
                8

            Length of cyclic pattern defined equal to period of the pattern.

        ..  container:: example

            **Example 2.** Gets length of acyclic pattern:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 2, 3],
                ...     )

            ::

                >>> len(pattern)
                4

            Length of acyclic pattern defined equal to greatest index in
            pattern, plus 1.

        ..  container:: example

            **Example 3.** Gets length of pattern with negative indices:

            ::

                >>> pattern = patterntools.Pattern(
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

    def __or__(self, other):
        r'''Logical OR of two patterns.

        ..  container:: example

            **Example.**

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

        Returns compound pattern.
        '''
        from abjad.tools import patterntools
        return patterntools.CompoundPattern([self, other], operator='or')

    def __xor__(self, other):
        r'''Logical XOR of two patterns.

        ..  container:: example

            **Example.**

            ::

                >>> pattern_1 = patterntools.select_first(3)
                >>> pattern_2 = patterntools.select_last(3)
                >>> pattern = pattern_1 ^ pattern_2

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
                    operator='xor',
                    )

        Returns compound pattern.
        '''
        from abjad.tools import patterntools
        return patterntools.CompoundPattern([self, other], operator='xor')

    ### PUBLIC METHODS ###

    @classmethod
    def from_vector(class_, vector):
        r'''Makes pattern from boolean `vector`.

        ..  container:: example

            **Example 1.** Matches three indices out of every five:

            ::

                >>> pattern = [1, 0, 0, 1, 1]
                >>> pattern = patterntools.Pattern.from_vector(pattern)
                >>> print(format(pattern))
                patterntools.Pattern(
                    indices=(0, 3, 4),
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

            **Example 2.** Matches three indices out of every six:

            ::

                >>> pattern = [1, 0, 0, 1, 1, 0]
                >>> pattern = patterntools.Pattern.from_vector(pattern)
                >>> print(format(pattern))
                patterntools.Pattern(
                    indices=(0, 3, 4),
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

            **Example 1.** Gets boolean vector of acyclic pattern:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 2.** Gets vector of cyclic pattern:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 3.** Gets vector of inverted pattern:

            ::

                >>> pattern = patterntools.Pattern(
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

        Returns list of ones and zeroes.
        '''
        total_length = total_length or len(self)
        boolean_vector = []
        for index in range(total_length):
            result = self.matches_index(index, total_length)
            boolean_vector.append(int(result))
        return boolean_vector

    def matches_index(self, index, total_length, rotation=None):
        r'''Is true when pattern matches `index` taken under `total_length`.
        Otherwise false.

        ..  container:: example

            **Example 1a.** Matches three indices out of every eight:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 1b.** Matches three indices out of every eight, offset
            ``1`` to the left:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 1c.** Matches three indices out of every eight, offset
            ``2`` to the left:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 2a.** Matches three indices out of every sixteen:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 2b.** Matches three indices out of every sixteen, offset
            ``1`` to the left:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 2c.** Matches three indices out of every sixteen, offset
            ``2`` to the left:

            ::

                >>> pattern = patterntools.Pattern(
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

        Returns true or false.
        '''
        assert 0 <= total_length
        if 0 <= index:
            nonnegative_index = index
        else:
            nonnegative_index = total_length - abs(index)
        inverted = bool(self.inverted)
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

    def reverse(self):
        r'''Reverses pattern.

        ..  container:: example

            **Example 1.** Matches three indices out of every eight:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 2.** Reverses pattern:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern = pattern.reverse()
                >>> print(format(pattern))
                patterntools.Pattern(
                    indices=(-1, -2, -8),
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

        Returns new pattern.
        '''
        indices = [-index - 1 for index in self.indices]
        return new(self, indices=indices)

    def rotate(self, n=0):
        r'''Rotates pattern.

        ..  container:: example

            **Example 1.** Matches three indices out of every eight:

            ::

                >>> pattern = patterntools.Pattern(
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

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern = pattern.rotate(n=2)
                >>> print(format(pattern))
                patterntools.Pattern(
                    indices=(2, 3, 9),
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

            **Example 2.** Matches three indices out of every eight with
            negative indices:

            ::

                >>> pattern = patterntools.Pattern(
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

                >>> pattern = patterntools.Pattern(
                ...     indices=[-3, -2, -1],
                ...     period=8,
                ...     )

            ::

                >>> pattern = pattern.rotate(n=2)
                >>> print(format(pattern))
                patterntools.Pattern(
                    indices=(-1, 0, 1),
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

        Returns new pattern.
        '''
        indices = [index + n for index in self.indices]
        return new(self, indices=indices)

    ### PUBLIC PROPERTIES ###

    @property
    def indices(self):
        r'''Gets indices of pattern.

        ..  container:: example

            **Example 1.** Matches three indices out of every eight:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.indices
                (0, 1, 7)

        ..  container:: example

            **Example 2.** Matches three indices out of every sixteen:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

                >>> pattern.indices
                (0, 1, 7)

        Defaults to none.

        Set to integers or none.

        Returns integers or none.
        '''
        return self._indices

    @property
    def inverted(self):
        r'''Is true when pattern is inverted. Otherwise false.

        ..  container:: example

            **Example 1.** Matches three indices out of every eight:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 2.** Pattern that rejects three indices from every eight;
            equivalently, pattern matches ``8-3=5`` indices out of every eight:

            ::

                >>> pattern = patterntools.Pattern(
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

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._inverted

    @property
    def payload(self):
        r'''Gets payload of pattern.

        ..  container:: example

            **Example 1.** Pattern with rhythm-maker payload assigned to three
            of every eight indices:

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> pattern = patterntools.Pattern(
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

            **Example 1.** Pattern with a period of eight:

            ::

                >>> pattern = patterntools.Pattern(
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

            **Example 2.** Same pattern with a period of sixteen:

            ::

                >>> pattern = patterntools.Pattern(
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

        Defaults to none.

        Set to positive integer or none.

        Returns positive integer or none.
        '''
        return self._period

    @property
    def weight(self):
        r'''Gets weight of pattern.

        ..  container:: example

            **Example 1.** Gets weight of cyclic pattern:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.weight
                3

        ..  container:: example

            **Example 2.** Gets weight of acyclic pattern:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 2, 3],
                ...     )

            ::

                >>> pattern.weight
                3

        Weight defined equal to number of indices in pattern.

        Returns nonnegative integer.
        '''
        return len(self.indices)
