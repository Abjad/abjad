from abjad.tools.pitchtools.ObjectVector import ObjectVector


class NamedChromaticPitchVector(ObjectVector):
    '''.. versionadded:: 2.0

    Abjad model of named chromatic pitch vector::

        >>> named_chromatic_pitch_vector = pitchtools.NamedChromaticPitchVector(
        ...     ["c''", "c''", "cs''", "cs''", "cs''"])

    ::

        >>> named_chromatic_pitch_vector
        NamedChromaticPitchVector(c'': 2, cs'': 3)

    ::

        >>> print named_chromatic_pitch_vector
        NamedChromaticPitchVector(c'': 2, cs'': 3)

    Named chromatic pitch vectors are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = (["c''", "c''", "cs''", "cs''", "cs''"], )

    ### INITIALIZER ###

    def __init__(self, pitch_tokens):
        from abjad.tools import pitchtools
        for token in pitch_tokens:
            pitch = pitchtools.NamedChromaticPitch(token)
            try:
                dict.__setitem__(self, str(pitch), self[str(pitch)] + 1)
            except KeyError:
                dict.__setitem__(self, str(pitch), 1)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        pitches = self.named_chromatic_pitches
        if not pitches:
            return ' '
        substrings = []
        for pitch in pitches:
            count = self[str(pitch)]
            substring = '%s: %s' % (pitch, count)
            substrings.append(substring)
        return ', '.join(substrings)

    ### PUBLIC PROPERTIES ###

    @property
    def chromatic_pitch_numbers(self):
        numbers = []
        for pitch in self.named_chromatic_pitches:
            number = pitch.chromatic_pitch_number
            if number not in numbers:
                numbers.append(number)
        numbers.sort()
        return numbers

    @property
    def named_chromatic_pitches(self):
        from abjad.tools import pitchtools
        pitches = [pitchtools.NamedChromaticPitch(key) for key, value in self.items()]
        pitches.sort()
        return pitches
