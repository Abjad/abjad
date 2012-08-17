from abjad.tools.pitchtools.ObjectVector import ObjectVector


class NumberedChromaticPitchClassVector(ObjectVector):
    '''.. versionadded:: 2.0

    Abjad model of numbered chromatic pitch-class vector::

        >>> ncpcv = pitchtools.NumberedChromaticPitchClassVector(
        ...     [13, 13, 14.5, 14.5, 14.5, 6, 6, 6])

    ::

        >>> print ncpcv
        0 2 0 0 0 0 | 3 0 0 0 0 0
        0 0 3 0 0 0 | 0 0 0 0 0 0

    Numbered chromatic pitch-class vectors are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = ([13, 13, 14.5, 14.5, 14.5, 6, 6, 6], )

    ### INITIALIZER ###

    def __init__(self, pitch_class_tokens):
        from abjad.tools import pitchtools
        for pcn in range(12):
            dict.__setitem__(self, pcn, 0)
            dict.__setitem__(self, pcn + 0.5, 0)
        for token in pitch_class_tokens:
            pitch_class = pitchtools.NumberedChromaticPitchClass(token)
            dict.__setitem__(self, abs(pitch_class), self[abs(pitch_class)] + 1)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __str__(self):
        string = self._twelve_tone_format_string
        if self._has_quartertones:
            string += '\n%s' % self._quartertone_format_string
        return string

    ### PRIVATE PROPERTIES ###

    @property
    def _first_quartertone_sextet_string(self):
        items = self._quartertone_items[:6]
        substrings = []
        for pitch_class_number, count in sorted(items):
            substring = '%s' % count
            substrings.append(substring)
        return ' '.join(substrings)

    @property
    def _first_twelve_tone_sextet_string(self):
        items = self._twelve_tone_items[:6]
        substrings = []
        for pitch_class_number, count in sorted(items):
            substring = '%s' % count
            substrings.append(substring)
        return ' '.join(substrings)

    @property
    def _format_string(self):
        string = self._twelve_tone_format_string
        if self._has_quartertones:
            string += ' || %s' % self._quartertone_format_string
        return string

    @property
    def _has_quartertones(self):
        return any([0 < item[1] for item in self._quartertone_items])

    @property
    def _quartertone_format_string(self):
        return '%s | %s' % (
            self._first_quartertone_sextet_string,
            self._second_quartertone_sextet_string)

    @property
    def _quartertone_items(self):
        items = [item for item in self.items() if isinstance(item[0], float)]
        items.sort()
        return items

    @property
    def _second_quartertone_sextet_string(self):
        items = self._quartertone_items[6:]
        substrings = []
        for pitch_class_number, count in sorted(items):
            substring = '%s' % count
            substrings.append(substring)
        return ' '.join(substrings)

    @property
    def _second_twelve_tone_sextet_string(self):
        items = self._twelve_tone_items[6:]
        substrings = []
        for pitch_class_number, count in sorted(items):
            substring = '%s' % count
            substrings.append(substring)
        return ' '.join(substrings)

    @property
    def _twelve_tone_format_string(self):
        return '%s | %s' % (
            self._first_twelve_tone_sextet_string,
            self._second_twelve_tone_sextet_string)

    @property
    def _twelve_tone_items(self):
        items = [item for item in self.items() if isinstance(item[0], int)]
        items.sort()
        return items

    ### PUBLIC PROPERTIES ###

    @property
    def chromatic_pitch_class_numbers(self):
        '''Read-only chromatic pitch-class numbers from numbered chromatic 
        pitch-class vector::

            >>> ncpcv.chromatic_pitch_class_numbers
            [1, 2.5, 6]

        Return list.
        '''
        numbers = [abs(pitch_class) for pitch_class in self.numbered_chromatic_pitch_classes]
        numbers.sort()
        return numbers

    @property
    def numbered_chromatic_pitch_classes(self):
        '''Read-only numbered chromatic pitch-classes from numbered chromatic pitch-class vector::

            >>> result = ncpcv.numbered_chromatic_pitch_classes

        ::

            >>> for x in result: x
            ...
            NumberedChromaticPitchClass(2.5) 
            NumberedChromaticPitchClass(1) 
            NumberedChromaticPitchClass(6)

        Return list.
        '''
        from abjad.tools import pitchtools
        pitch_classes = []
        for pitch_class_number, count in self.items():
            if 0 < count:
                pitch_class = pitchtools.NumberedChromaticPitchClass(pitch_class_number)
                pitch_classes.append(pitch_class)
        return pitch_classes
