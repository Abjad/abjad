from abjad.system.AbjadValueObject import AbjadValueObject
from .NumberedPitchClass import NumberedPitchClass


class ColorMap(AbjadValueObject):
    """
    Color map.

    ..  container:: example

        Maps pitch-classes to red, green and blue:

        >>> color_map = abjad.ColorMap(
        ...     colors=['red', 'green', 'blue'],
        ...     pitch_iterables=[
        ...         [-8, 2, 10, 21],
        ...         [0, 11, 32, 41],
        ...         [15, 25, 42, 43],
        ...         ],
        ...     )

        >>> abjad.f(color_map)
        abjad.ColorMap(
            colors=['red', 'green', 'blue'],
            pitch_iterables=[
                [-8, 2, 10, 21],
                [0, 11, 32, 41],
                [15, 25, 42, 43],
                ],
            )

    Color maps are immutable.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_color_dictionary',
        '_colors',
        '_pitch_iterables',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, *, colors=None, pitch_iterables=None):
        pitch_iterables = pitch_iterables or []
        colors = colors or []
        assert len(pitch_iterables) == len(colors)
        self._pitch_iterables = pitch_iterables
        self._colors = colors
        self._color_dictionary = {}
        self._initialize_color_dictionary()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        """
        Formats color map.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=['red', 'green', 'blue'],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...         ],
            ...     )

            >>> abjad.f(color_map)
            abjad.ColorMap(
                colors=['red', 'green', 'blue'],
                pitch_iterables=[
                    [-8, 2, 10, 21],
                    [0, 11, 32, 41],
                    [15, 25, 42, 43],
                    ],
                )

        Returns string.
        """
        return super().__format__(format_specification=format_specification)

    def __getitem__(self, pitch_class):
        """
        Gets `pitch_class` color.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=['red', 'green', 'blue'],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...         ],
            ...     )

            >>> color_map[11]
            'green'

        Returns string.
        """
        pitch_class = NumberedPitchClass(pitch_class)
        return self._color_dictionary[pitch_class.number]

    ### PRIVATE METHODS ###

    def _initialize_color_dictionary(self):
        for pitch_iterable, color in zip(self.pitch_iterables, self.colors):
            for pitch in pitch_iterable:
                pc = NumberedPitchClass(pitch)
                keys = self._color_dictionary.keys()
                if pc.number in list(keys):
                    print(pc, list(self._color_dictionary.keys()))
                    message = 'duplicated pitch-class in color map: {!r}.'
                    message = message.format(pc)
                    raise KeyError(message)
                self._color_dictionary[pc.number] = color

    ### PUBLIC PROPERTIES ###

    @property
    def colors(self):
        """
        Gets colors.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=['red', 'green', 'blue'],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...         ],
            ...     )

            >>> color_map.colors
            ['red', 'green', 'blue']

        Returns list.
        """
        return self._colors

    @property
    def is_twelve_tone_complete(self):
        """
        Is true when color map contains all 12-ET pitch-classes.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=['red', 'green', 'blue'],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...         ],
            ...     )

            >>> color_map.is_twelve_tone_complete
            True

        Return boolean.
        """
        pcs = range(12)
        return set(pcs).issubset(set(self._color_dictionary.keys()))

    @property
    def is_twenty_four_tone_complete(self):
        """
        Is true when color map contains all 24-ET pitch-classes.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=['red', 'green', 'blue'],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...         ],
            ...     )

            >>> color_map.is_twenty_four_tone_complete
            False

        Return boolean.
        """
        pcs = [x / 2.0 for x in range(24)]
        pcs = [int(x) if int(x) == x else x for x in pcs]
        return set(pcs).issubset(set(self._color_dictionary.keys()))

    @property
    def pairs(self):
        """
        Gets pairs.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=['red', 'green', 'blue'],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...         ],
            ...     )

            >>> for pair in color_map.pairs:
            ...     pair
            ...
            (0, 'green')
            (1, 'blue')
            (2, 'red')
            (3, 'blue')
            (4, 'red')
            (5, 'green')
            (6, 'blue')
            (7, 'blue')
            (8, 'green')
            (9, 'red')
            (10, 'red')
            (11, 'green')

        Returns list.
        """
        items = list(self._color_dictionary.items())
        return list(sorted(items))

    @property
    def pitch_iterables(self):
        """
        Gets pitch iterables.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=['red', 'green', 'blue'],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...         ],
            ...     )

            >>> color_map.pitch_iterables
            [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]

        Returns list.
        """
        return self._pitch_iterables

    ### PUBLIC METHODS ###

    def get(self, key, alternative=None):
        """
        Gets `key` from color map.

        ..  container:: example

            >>> color_map = abjad.ColorMap(
            ...     colors=['red', 'green', 'blue'],
            ...     pitch_iterables=[
            ...         [-8, 2, 10, 21],
            ...         [0, 11, 32, 41],
            ...         [15, 25, 42, 43],
            ...         ],
            ...     )

            >>> color_map.get(11)
            'green'

        Returns `alternative` when `key` is not found.

        Returns string.
        """
        try:
            return self[key]
        except (KeyError, TypeError, ValueError):
            return alternative
