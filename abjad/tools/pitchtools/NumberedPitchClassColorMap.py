# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


# TODO: implement __illustrate__
class NumberedPitchClassColorMap(AbjadValueObject):
    '''Numbered pitch-class color map.

    ..  container:: example

        **Example 1.** Maps pitch-classes to red, green and blue:

        ::

            >>> pitches = [
            ...     [-8, 2, 10, 21],
            ...     [0, 11, 32, 41],
            ...     [15, 25, 42, 43],
            ...     ]
            >>> colors = ['red', 'green', 'blue']
            >>> color_map = pitchtools.NumberedPitchClassColorMap(pitches, colors)

    Numbered pitch-class color maps are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_color_dictionary',
        '_colors',
        '_pitch_iterables',
        )

    ### INITIALIZER ###

    def __init__(self, pitch_iterables=None, colors=None):
        pitch_iterables = pitch_iterables or []
        colors = colors or []
        assert len(pitch_iterables) == len(colors)
        self._pitch_iterables = pitch_iterables
        self._colors = colors
        self._color_dictionary = {}
        self._initialize_color_dictionary()

    ### SPECIAL METHODS ###

    def __getitem__(self, pc):
        r'''Gets color corresponding to `pc` in color map.

        ::

            >>> color_map[11]
            'green'

        Returns string.
        '''
        from abjad.tools import pitchtools
        pc = pitchtools.NumberedPitchClass(pc)
        color = self._color_dictionary[pc.pitch_class_number]
        return color

    ### PRIVATE METHODS ###

    def _initialize_color_dictionary(self):
        from abjad.tools import pitchtools
        for pitch_iterable, color in zip(self.pitch_iterables, self.colors):
            for pitch in pitch_iterable:
                pc = pitchtools.NumberedPitchClass(pitch)
                if pc.pitch_class_number in list(self._color_dictionary.keys()):
                    print(pc, list(self._color_dictionary.keys()))
                    message = 'duplicated pitch-class in color map: {!r}.'
                    message = message.format(pc)
                    raise KeyError(message)
                self._color_dictionary[pc.pitch_class_number] = color

    ### PUBLIC METHODS ###

    def get(self, key, alternative=None):
        r'''Gets `key` from color map.

        ::

            >>> color_map.get(11)
            'green'

        Returns `alternative` when `key` is not found.

        Returns string.
        '''
        try:
            return self[key]
        except (KeyError, TypeError, ValueError):
            return alternative

    ### PUBLIC PROPERTIES ###

    @property
    def colors(self):
        r'''Colors of color map.

        ::

            >>> color_map.colors
            ['red', 'green', 'blue']

        Returns list.
        '''
        return self._colors

    @property
    def is_twelve_tone_complete(self):
        r'''Is true when color map contains all 12-ET pitch-classes.

        ::

            >>> color_map.is_twelve_tone_complete
            True

        Return boolean.
        '''
        pcs = range(12)
        return set(pcs).issubset(set(self._color_dictionary.keys()))

    @property
    def is_twenty_four_tone_complete(self):
        r'''Is true when color map contains all 24-ET pitch-classes.

        ::

            >>> color_map.is_twenty_four_tone_complete
            False

        Return boolean.
        '''
        pcs = [x / 2.0 for x in range(24)]
        pcs = [int(x) if int(x) == x else x for x in pcs]
        return set(pcs).issubset(set(self._color_dictionary.keys()))

    @property
    def pairs(self):
        r'''Pairs of color map.

        ::

            >>> for pair in color_map.pairs:
            ...     pair
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
        '''
        items = list(self._color_dictionary.items())
        return list(sorted(items))

    @property
    def pitch_iterables(self):
        r'''Pitch interables of color map.

        ::

            >>> color_map.pitch_iterables
            [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]

        Returns ?
        '''
        return self._pitch_iterables
