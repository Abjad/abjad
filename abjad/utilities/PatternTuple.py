from .TypedTuple import TypedTuple


class PatternTuple(TypedTuple):
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

        >>> abjad.f(patterns)
        abjad.PatternTuple(
            (
                abjad.Pattern(
                    indices=[0, 1, 7],
                    period=10,
                    ),
                abjad.Pattern(
                    indices=[-2, -1],
                    ),
                abjad.Pattern(
                    indices=[2],
                    period=3,
                    ),
                )
            )

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

        >>> abjad.f(patterns)
        abjad.PatternTuple(
            (
                abjad.Pattern(
                    indices=[1],
                    period=2,
                    ),
                abjad.Pattern(
                    indices=[-3, -2, -1],
                    ),
                )
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

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
            1 Pattern(indices=[1], period=2)
            2 None
            3 Pattern(indices=[1], period=2)
            4 None
            5 Pattern(indices=[1], period=2)
            6 None
            7 Pattern(indices=[-3, -2, -1])
            8 Pattern(indices=[-3, -2, -1])
            9 Pattern(indices=[-3, -2, -1])

            Last three indices match the second pattern.

            Gets patterns that match next ten indices:

            >>> for i in range(10, 20):
            ...     match = patterns.get_matching_pattern(i, 10)
            ...     print(i, match)
            ...
            10 None
            11 Pattern(indices=[1], period=2)
            12 None
            13 Pattern(indices=[1], period=2)
            14 None
            15 Pattern(indices=[1], period=2)
            16 None
            17 Pattern(indices=[1], period=2)
            18 None
            19 Pattern(indices=[1], period=2)

            Last three indices no longer match the second pattern.

        ..  container:: example

            Gets patterns that match the first ten indices, with rotation set
            to ``1``:

            >>> for i in range(10):
            ...     match = patterns.get_matching_pattern(i, 10, rotation=1)
            ...     print(i, match)
            ...
            0 Pattern(indices=[1], period=2)
            1 None
            2 Pattern(indices=[1], period=2)
            3 None
            4 Pattern(indices=[1], period=2)
            5 None
            6 Pattern(indices=[1], period=2)
            7 Pattern(indices=[-3, -2, -1])
            8 Pattern(indices=[-3, -2, -1])
            9 Pattern(indices=[-3, -2, -1])

            Matching indices of first pattern offset by ``1``.

            Gets patterns that match next ten indices with rotation set to
            ``1``:

            >>> for i in range(10, 20):
            ...     match = patterns.get_matching_pattern(i, 10, rotation=1)
            ...     print(i, match)
            ...
            10 Pattern(indices=[1], period=2)
            11 None
            12 Pattern(indices=[1], period=2)
            13 None
            14 Pattern(indices=[1], period=2)
            15 None
            16 Pattern(indices=[1], period=2)
            17 None
            18 Pattern(indices=[1], period=2)
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
            0 Pattern(indices=[-3], inverted=True)
            1 Pattern(indices=[-3], inverted=True)
            2 Pattern(indices=[-3], inverted=True)
            3 Pattern(indices=[-3], inverted=True)
            4 Pattern(indices=[-3], inverted=True)
            5 Pattern(indices=[-3], inverted=True)
            6 Pattern(indices=[-3], inverted=True)
            7 None
            8 Pattern(indices=[-3], inverted=True)
            9 Pattern(indices=[-3], inverted=True)

        Returns pattern or none.
        """
        for pattern in reversed(self):
            if hasattr(pattern, 'pattern'):
                if pattern.pattern.matches_index(
                    index, total_length, rotation=rotation):
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

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        import abjad

        def coerce_(argument):
            if hasattr(argument, 'pattern'):
                pass
            elif not isinstance(argument, abjad.Pattern):
                argument = abjad.Pattern(*argument)
            return argument
        return coerce_
