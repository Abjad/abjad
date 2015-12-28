# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools.new import new


class Pattern(AbjadValueObject):
    r'''Pattern.

    ..  container:: example

        **Example 1.** Pattern that matches three indices out of every eight:

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

        **Example 2.** Pattern that matches three indices out of every
        sixteen:

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

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Masks'

    __slots__ = (
        '_indices',
        '_invert',
        '_payload',
        '_period',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        indices=None,
        invert=None,
        payload=None,
        period=None,
        ):
        if indices is not None:
            assert all(isinstance(_, int) for _ in indices), repr(indices)
            indices = tuple(indices)
        self._indices = indices
        if invert is not None:
            invert = bool(invert)
        self._invert = invert
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
                    invert=True,
                    )

            ::

                >>> pattern = ~pattern
                >>> print(format(pattern))
                patterntools.Pattern(
                    indices=(0, 1, 2),
                    invert=False,
                    )
                    
            Negation defined equal to inversion.

        Returns new pattern.
        '''
        invert = not self.invert
        pattern = new(self, invert=invert)
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

    ### PUBLIC PROPERTIES ###

    @property
    def vector(self):
        r'''Gets vector pattern.
        
        ..  container:: example

            **Example 1.** Gets vector of cyclic pattern:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.vector
                [1, 1, 0, 0, 0, 0, 0, 1]

        ..  container:: example

            **Example 2.** Gets vector of acyclic pattern:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 2, 3],
                ...     )

            ::

                >>> pattern.vector
                [1, 0, 1, 1]

        Vector defined equal to list of ones and zeroes with length equal to
        length of pattern.

        Returns list.
        '''
        result = []
        for i in range(len(self)):
            if i in self.indices:
                result.append(1)
            else:
                result.append(0)
        return result

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

    ### PUBLIC METHODS ###

    @classmethod
    def from_vector(class_, vector):
        r'''Makes pattern from boolean `vector`.

        ..  container:: example

            **Example 1.** Pattern that matches three indices out of every
            five:

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

            **Example 2.** Pattern that matches three indices out of every
            six:

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

    def matches_index(self, index, total_length, rotation=None):
        r'''Is true when pattern matches `index` taken under `total_length`.
        Otherwise false.

        ..  container:: example

            **Example 1a.** Pattern that matches three indices out of every 
            eight:

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

            **Example 1b.** Pattern that matches three indices out of every 
            eight, offset ``1`` to the left:

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

            **Example 1c.** Pattern that matches three indices out of every 
            eight, offset ``2`` to the left:

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

            **Example 2a.** Pattern that matches three indices out of every
            sixteen:

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

            **Example 2b.** Pattern that matches three indices out of every
            sixteen, offset ``1`` to the left:

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

            **Example 2c.** Pattern that matches three indices out of every
            sixteen, offset ``2`` to the left:

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
        invert = bool(self.invert)
        if self.period is None:
            for index in self.indices:
                if index < 0:
                    index = total_length - abs(index)
                if index == nonnegative_index and index < total_length:
                    return True ^ invert
        else:
            if rotation is not None:
                nonnegative_index += rotation
            nonnegative_index = nonnegative_index % self.period
            for index in self.indices:
                if index < 0:
                    index = total_length - abs(index)
                    index = index % self.period
                if index == nonnegative_index and index < total_length:
                    return True ^ invert
        return False ^ invert

    ### PUBLIC PROPERTIES ###

    @property
    def indices(self):
        r'''Gets indices of pattern.

        ..  container:: example

            **Example 1.** Pattern that matches three indices out of every
            eight:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.indices
                (0, 1, 7)

        ..  container:: example

            **Example 2.** Pattern that matches three indices out of every
            sixteen:

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
    def invert(self):
        r'''Gets inversion flag of pattern.

        ..  container:: example

            **Example 1.** Pattern that matches three indices out of every
            eight:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.invert is None
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
                ...     invert=True
                ...     )

            ::

                >>> pattern.invert
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

        Set to boolean or none.

        Returns boolean or none.
        '''
        return self._invert

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