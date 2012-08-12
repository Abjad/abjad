from abjad.tools.abctools import AbjadObject


class NumberedChromaticPitchClassColorMap(AbjadObject):
    '''.. versionadded:: 2.0

    Abjad model of a numbered chromatic pitch-class color map::

        >>> chromatic_pitch_class_numbers = [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
        >>> colors = ['red', 'green', 'blue']
        >>> mapping = pitchtools.NumberedChromaticPitchClassColorMap(
        ... chromatic_pitch_class_numbers, colors)

    Numbered chromatic pitch-class color maps are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_color_dictionary', '_colors', '_pitch_iterables', )

    ### INITIALIZER ###

    def __init__(self, pitch_iterables, colors):
        assert len(pitch_iterables) == len(colors)
        object.__setattr__(self, '_pitch_iterables', pitch_iterables)
        object.__setattr__(self, '_colors', colors)
        object.__setattr__(self, '_color_dictionary', {})
        self._init_color_dictionary()

    ### SPECIAL METHODS ###

    def __getitem__(self, pc):
        from abjad.tools import pitchtools
        pc = pitchtools.NumberedChromaticPitchClass(pc)
        color = self._color_dictionary[abs(pc)]
        return color

    def __repr__(self):
        sorted_keys = self._color_dictionary.keys()
        sorted_keys.sort()
        return '%s(%s, %s)' % (type(self).__name__, self._pitch_iterables, self._colors)

    ### PRIVATE METHODS ###

    def _init_color_dictionary(self):
        from abjad.tools import pitchtools
        for pitch_iterable, color in zip(self.pitch_iterables, self.colors):
            for pitch in pitch_iterable:
                pc = pitchtools.NumberedChromaticPitchClass(pitch)
                if abs(pc) in self._color_dictionary.keys():
                    print pc, self._color_dictionary.keys()
                    raise KeyError('Duplicated pitch-class %s in color dictionary.' % pc)
                self._color_dictionary[abs(pc)] = color

    ### PUBLIC PROPERTIES ###

    @property
    def colors(self):
        return self._colors

    @property
    def pairs(self):
        items = self._color_dictionary.items()
        return list(sorted(items))

    @property
    def pitch_iterables(self):
        return self._pitch_iterables

    @property
    def twelve_tone_complete(self):
        pcs = range(12)
        return set(pcs).issubset(set(self._color_dictionary.keys()))

    @property
    def twenty_four_tone_complete(self):
        pcs = [x / 2.0 for x in range(24)]
        pcs = [int(x) if int(x) == x else x for x in pcs]
        return set(pcs).issubset(set(self._color_dictionary.keys()))

    ### PUBLIC METHODS ###

    def get(self, key, alternative=None):
        try:
            return self[key]
        except (KeyError, TypeError, ValueError):
            return alternative
