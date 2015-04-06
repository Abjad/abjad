# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class BooleanPatternInventory(TypedTuple):
    r'''Ordered list of boolean patterns.

    ..  container:: example

        **Example 1.** Inventory of three patterns:

        ::

            >>> inventory = rhythmmakertools.BooleanPatternInventory([
            ...     rhythmmakertools.BooleanPattern(
            ...         indices=[0, 1, 7],
            ...         period=10,
            ...         ),
            ...     rhythmmakertools.BooleanPattern(
            ...         indices=[-2, -1],
            ...         ),
            ...     rhythmmakertools.BooleanPattern(
            ...         indices=[2],
            ...         period=3,
            ...         start=1,
            ...         stop=-1,
            ...         ),
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

    ..  container:: example

        **Example 2.** Inventory of two patterns:

        ::

            >>> inventory = rhythmmakertools.BooleanPatternInventory([
            ...     rhythmmakertools.BooleanPattern(
            ...         indices=[1],
            ...         period=2,
            ...         ),
            ...     rhythmmakertools.BooleanPattern(
            ...         indices=[-3, -2, -1],
            ...         ),
            ...     ])

        ::

            >>> print(format(inventory))
            rhythmmakertools.BooleanPatternInventory(
                (
                    rhythmmakertools.BooleanPattern(
                        indices=(1,),
                        period=2,
                        ),
                    rhythmmakertools.BooleanPattern(
                        indices=(-3, -2, -1),
                        ),
                    )
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    def get_matching_pattern(self, index, total_length, seed=None):
        r'''Gets pattern matching `index`.

        ..  container:: example

            Inventory of two patterns:

            ::

                >>> inventory = rhythmmakertools.BooleanPatternInventory([
                ...     rhythmmakertools.BooleanPattern(
                ...         indices=[1],
                ...         period=2,
                ...         ),
                ...     rhythmmakertools.BooleanPattern(
                ...         indices=[-3, -2, -1],
                ...         ),
                ...     ])

            **Example 1a.** Gets patterns that match the first ten indices:

            ::

                >>> for i in range(10):
                ...     match = inventory.get_matching_pattern(i, 10)
                ...     print(i, match)
                ...
                0 None
                1 BooleanPattern(indices=(1,), period=2)
                2 None
                3 BooleanPattern(indices=(1,), period=2)
                4 None
                5 BooleanPattern(indices=(1,), period=2)
                6 None
                7 BooleanPattern(indices=(-3, -2, -1))
                8 BooleanPattern(indices=(-3, -2, -1))
                9 BooleanPattern(indices=(-3, -2, -1))

            Last three indices match the second pattern.

            **Example 1b.** Gets patterns that match next ten indices:

            ::

                >>> for i in range(10, 20):
                ...     match = inventory.get_matching_pattern(i, 10)
                ...     print(i, match)
                ...
                10 None
                11 BooleanPattern(indices=(1,), period=2)
                12 None
                13 BooleanPattern(indices=(1,), period=2)
                14 None
                15 BooleanPattern(indices=(1,), period=2)
                16 None
                17 BooleanPattern(indices=(1,), period=2)
                18 None
                19 BooleanPattern(indices=(1,), period=2)

            Last three indices no longer match the second pattern.

        ..  container:: example

            **Example 2a.** Gets patterns that match the first ten indices,
            with seed set to ``1``:

            ::

                >>> for i in range(10):
                ...     match = inventory.get_matching_pattern(i, 10, seed=1)
                ...     print(i, match)
                ...
                0 BooleanPattern(indices=(1,), period=2)
                1 None
                2 BooleanPattern(indices=(1,), period=2)
                3 None
                4 BooleanPattern(indices=(1,), period=2)
                5 None
                6 BooleanPattern(indices=(1,), period=2)
                7 BooleanPattern(indices=(-3, -2, -1))
                8 BooleanPattern(indices=(-3, -2, -1))
                9 BooleanPattern(indices=(-3, -2, -1))

            Matching indices of first pattern offset by ``1``.

            **Example 1b.** Gets patterns that match next ten indices with seed
            set to ``1``:

            ::

                >>> for i in range(10, 20):
                ...     match = inventory.get_matching_pattern(i, 10, seed=1)
                ...     print(i, match)
                ...
                10 BooleanPattern(indices=(1,), period=2)
                11 None
                12 BooleanPattern(indices=(1,), period=2)
                13 None
                14 BooleanPattern(indices=(1,), period=2)
                15 None
                16 BooleanPattern(indices=(1,), period=2)
                17 None
                18 BooleanPattern(indices=(1,), period=2)
                19 None

            Matching indices of first pattern offset by ``1``.

        Returns pattern or none.
        '''
        for pattern in reversed(self):
            if pattern.matches_index(index, total_length, seed=seed):
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