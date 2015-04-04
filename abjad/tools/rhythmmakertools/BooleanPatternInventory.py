# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class BooleanPatternInventory(TypedTuple):
    r'''An ordered list of boolean patterns.

    ::

        >>> inventory = rhythmmakertools.BooleanPatternInventory([
        ...     rhythmmakertools.BooleanPattern([0, 1, 7], 10),
        ...     rhythmmakertools.BooleanPattern([-2, -1]),
        ...     rhythmmakertools.BooleanPattern([2], 3, 1, -1),
        ...     ])

    ::

        >>> print(format(inventory))
        rhythmmakertools.BooleanPatternInventory(
            (
                rhythmmakertools.BooleanPattern(
                    indices=(0, 1, 7),
                    period=10,
                    ),
                rhythmmakertools.BooleanPattern(
                    indices=(-2, -1),
                    ),
                rhythmmakertools.BooleanPattern(
                    indices=(2,),
                    period=3,
                    start=1,
                    stop=-1,
                    ),
                )
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    def get_matching_pattern(self, index, total_length, seed=None):
        r'''Gets pattern matching `index`.

        ::

            >>> for i in range(11):
            ...     match = inventory.get_matching_pattern(i, 10)
            ...     print(i, match)
            ...
            0 BooleanPattern(indices=(0, 1, 7), period=10)
            1 BooleanPattern(indices=(0, 1, 7), period=10)
            2 None
            3 BooleanPattern(indices=(2,), period=3, start=1, stop=-1)
            4 None
            5 None
            6 BooleanPattern(indices=(2,), period=3, start=1, stop=-1)
            7 BooleanPattern(indices=(0, 1, 7), period=10)
            8 BooleanPattern(indices=(-2, -1))
            9 BooleanPattern(indices=(-2, -1))
            10 BooleanPattern(indices=(0, 1, 7), period=10)

        ::

            >>> for i in range(11):
            ...     match = inventory.get_matching_pattern(i, 10, seed=1)
            ...     print(i, match)
            ...
            0 BooleanPattern(indices=(0, 1, 7), period=10)
            1 None
            2 BooleanPattern(indices=(2,), period=3, start=1, stop=-1)
            3 None
            4 None
            5 BooleanPattern(indices=(2,), period=3, start=1, stop=-1)
            6 BooleanPattern(indices=(0, 1, 7), period=10)
            7 None
            8 BooleanPattern(indices=(2,), period=3, start=1, stop=-1)
            9 BooleanPattern(indices=(-2, -1))
            10 BooleanPattern(indices=(0, 1, 7), period=10)

        Returns pattern or none.
        '''
        for pattern in reversed(self):
            if pattern._matches_index(index, total_length, seed=seed):
                return pattern

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import rhythmmakertools
        def coerce_(expr):
            if not isinstance(expr, rhythmmakertools.BooleanPattern):
                expr = rhythmmakertools.BooleanPattern(*expr)
            return expr
        return coerce_