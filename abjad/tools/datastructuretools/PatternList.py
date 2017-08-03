# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class PatternList(TypedTuple):
    r'''Pattern list.

    ::

        >>> import abjad
        >>> from abjad.tools import rhythmmakertools

    ..  container:: example

        Three patterns:

        ::

            >>> patterns = abjad.PatternList([
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

        ::

            >>> f(patterns)
            abjad.PatternList(
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

        ::

            >>> patterns = abjad.PatternList([
            ...     abjad.Pattern(
            ...         indices=[1],
            ...         period=2,
            ...         ),
            ...     abjad.Pattern(
            ...         indices=[-3, -2, -1],
            ...         ),
            ...     ])

        ::

            >>> f(patterns)
            abjad.PatternList(
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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    def get_matching_pattern(self, index, total_length, rotation=None):
        r'''Gets pattern matching `index`.

        ..  container:: example

            Two patterns:

            ::

                >>> patterns = abjad.PatternList([
                ...     abjad.Pattern(
                ...         indices=[1],
                ...         period=2,
                ...         ),
                ...     abjad.Pattern(
                ...         indices=[-3, -2, -1],
                ...         ),
                ...     ])

            Gets patterns that match the first ten indices:

            ::

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

            ::

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

            ::

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

            ::

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

            ::

                >>> patterns = abjad.PatternList([
                ...     abjad.Pattern(
                ...         indices=[-3],
                ...         inverted=True,
                ...         ),
                ...     ])

            ::

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
        '''
        from abjad.tools import rhythmmakertools
        prototype = (
            rhythmmakertools.SilenceMask,
            rhythmmakertools.SustainMask,
            )
        for pattern in reversed(self):
            if isinstance(pattern, prototype):
                if pattern.pattern.matches_index(
                    index, total_length, rotation=rotation):
                    return pattern
            elif pattern.matches_index(index, total_length, rotation=rotation):
                return pattern

    def get_matching_payload(self, index, total_length, rotation=None):
        r'''Gets payload attached to pattern matching `index`.

        ..  container:: example

            Two patterns. Underlying notes with even divisions
            assigned to the last three indices:

            ::

                >>> patterns = abjad.PatternList([
                ...     abjad.Pattern(
                ...         indices=[0],
                ...         payload=rhythmmakertools.NoteRhythmMaker(),
                ...         period=1,
                ...         ),
                ...     abjad.Pattern(
                ...         indices=[-3, -2, -1],
                ...         payload=rhythmmakertools.EvenDivisionRhythmMaker(),
                ...         ),
                ...     ])

            Over ten indices:

            ::

                >>> for i in range(10):
                ...     match = patterns.get_matching_payload(i, 10)
                ...     print(i, match)
                ...
                0 NoteRhythmMaker()
                1 NoteRhythmMaker()
                2 NoteRhythmMaker()
                3 NoteRhythmMaker()
                4 NoteRhythmMaker()
                5 NoteRhythmMaker()
                6 NoteRhythmMaker()
                7 EvenDivisionRhythmMaker(denominators=[8], preferred_denominator='from_counts')
                8 EvenDivisionRhythmMaker(denominators=[8], preferred_denominator='from_counts')
                9 EvenDivisionRhythmMaker(denominators=[8], preferred_denominator='from_counts')

            Over fifteen indices:

            ::

                >>> for i in range(15):
                ...     match = patterns.get_matching_payload(i, 15)
                ...     print(i, match)
                ...
                0 NoteRhythmMaker()
                1 NoteRhythmMaker()
                2 NoteRhythmMaker()
                3 NoteRhythmMaker()
                4 NoteRhythmMaker()
                5 NoteRhythmMaker()
                6 NoteRhythmMaker()
                7 NoteRhythmMaker()
                8 NoteRhythmMaker()
                9 NoteRhythmMaker()
                10 NoteRhythmMaker()
                11 NoteRhythmMaker()
                12 EvenDivisionRhythmMaker(denominators=[8], preferred_denominator='from_counts')
                13 EvenDivisionRhythmMaker(denominators=[8], preferred_denominator='from_counts')
                14 EvenDivisionRhythmMaker(denominators=[8], preferred_denominator='from_counts')

        '''
        pattern = self.get_matching_pattern(index, total_length, rotation=rotation)
        payload = None
        if pattern:
            payload = pattern.payload
        return payload

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        def coerce_(argument):
            if isinstance(argument, prototype):
                pass
            elif not isinstance(argument, abjad.Pattern):
                argument = abjad.Pattern(*argument)
            return argument

        import abjad
        from abjad.tools import rhythmmakertools
        prototype = (
            rhythmmakertools.SilenceMask,
            rhythmmakertools.SustainMask,
            )
        return coerce_
