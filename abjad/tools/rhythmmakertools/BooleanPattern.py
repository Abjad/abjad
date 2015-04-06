# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class BooleanPattern(AbjadValueObject):
    r'''Boolean pattern.

    ..  container:: example

        **Example 1.** Pattern that matches three indices out of every eight:

        ::

            >>> pattern = rhythmmakertools.BooleanPattern(
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

            >>> pattern = rhythmmakertools.BooleanPattern(
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

    __slots__ = (
        '_indices',
        '_invert',
        '_period',
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        indices=None,
        invert=None,
        period=None,
        start=None,
        stop=None,
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
        self._period = period
        if start is not None:
            start = int(start)
        self._start = start
        if stop is not None:
            stop = int(stop)
        self._stop = stop

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from ide import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='indices',
                command='i',
                editor=idetools.getters.get_integers,
                ),
            systemtools.AttributeDetail(
                name='period',
                command='p',
                editor=idetools.getters.get_integer,
                ),
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_sequence(cls, sequence):
        r'''Makes boolean pattern from sequence.

        ..  container:: example

            **Example 1.** Pattern that matches three indices out of every
            five:

            ::

                >>> pattern = [1, 0, 0, 1, 1]
                >>> pattern = rhythmmakertools.BooleanPattern.from_sequence(pattern)
                >>> print(format(pattern))
                rhythmmakertools.BooleanPattern(
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
                >>> pattern = rhythmmakertools.BooleanPattern.from_sequence(pattern)
                >>> print(format(pattern))
                rhythmmakertools.BooleanPattern(
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

        Returns boolean pattern.
        '''
        sequence = [bool(_) for _ in sequence]
        period = len(sequence)
        indices = [i for i, x in enumerate(sequence) if x]
        return cls(
            period=period,
            indices=indices,
            )

    def matches_index(self, index, total_length, seed=None):
        r'''Is true when pattern matches `index` taken under `total_length`.
        Otherwise false.

        ..  container:: example

            **Example 1a.** Pattern that matches three indices out of every 
            eight:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
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

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> total_length = 16
                >>> for index in range(16):
                ...     match = pattern.matches_index(
                ...         index,
                ...         total_length,
                ...         seed=1,
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

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> total_length = 16
                >>> for index in range(16):
                ...     match = pattern.matches_index(
                ...         index,
                ...         total_length,
                ...         seed=2,
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

                >>> pattern = rhythmmakertools.BooleanPattern(
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

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

                >>> total_length = 16
                >>> for index in range(16):
                ...     match = pattern.matches_index(
                ...         index,
                ...         total_length,
                ...         seed=1,
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

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=16,
                ...     )

            ::

                >>> total_length = 16
                >>> for index in range(16):
                ...     match = pattern.matches_index(
                ...         index,
                ...         total_length,
                ...         seed=2,
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
        if self.start is not None or self.stop is not None:
            start, stop, _ = slice(self.start, self.stop).indices(total_length)
            if stop <= start:
                return False
            if self.start is not None and nonnegative_index < start:
                return False
            if self.stop is not None and stop <= nonnegative_index:
                return False
            nonnegative_index -= start
        if self.period is None:
            for index in self.indices:
                if index < 0:
                    index = total_length - abs(index)
                if index == nonnegative_index and index < total_length:
                    return True ^ invert
        else:
            if seed is not None:
                nonnegative_index += seed
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

                >>> pattern = rhythmmakertools.BooleanPattern(
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

                >>> pattern = rhythmmakertools.BooleanPattern(
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

                >>> pattern = rhythmmakertools.BooleanPattern(
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

                >>> pattern = rhythmmakertools.BooleanPattern(
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
    def period(self):
        r'''Gets period of pattern.

        ..  container:: example

            **Example 1.** Pattern with a period of eight:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
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

                >>> pattern = rhythmmakertools.BooleanPattern(
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
    def start(self):
        r'''Gets start index of pattern.

        ..  container:: example

            **Example 1.** Pattern that matches three indices out of every eight:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.start is None
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

            **Example 2.** Same pattern starting (offset by) one index later:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     start=1,
                ...     )

            ::

                >>> pattern.start
                1

            ::

                >>> total_length = 16
                >>> for index in range(16):
                ...     match = pattern.matches_index(index, total_length)
                ...     match = match or ''
                ...     print(index, match)
                0 
                1 True
                2 True
                3 
                4 
                5 
                6 
                7 
                8 True
                9 True
                10 True
                11 
                12 
                13 
                14 
                15 

            .. todo:: This looks wrong. Is this the intended behavior?

        Defaults to none.

        Set to integer or none.

        Returns integer or none.
        '''
        return self._start

    @property
    def stop(self):
        r'''Gets stop index of pattern.

        ..  container:: example

            **Example 1.** Pattern that matches three indices out of every
            eight:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     )

            ::

                >>> pattern.start is None
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

            **Example 2.** Same pattern but with the last index set to return
            false:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     stop=-1,
                ...     )

            ::

                >>> pattern.stop
                -1

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
                15 

        ..  container:: example

            **Example 3.** Same pattern but with the last ten indices set to
            false:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 1, 7],
                ...     period=8,
                ...     stop=-10,
                ...     )

            ::

                >>> pattern.stop
                -10

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
                7
                8
                9
                10 
                11 
                12 
                13 
                14 
                15 

        Defaults to none.

        Set to integer or none.

        Returns integer or none.
        '''
        return self._stop