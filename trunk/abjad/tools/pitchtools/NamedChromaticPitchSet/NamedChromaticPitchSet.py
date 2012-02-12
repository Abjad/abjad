from abjad.tools.pitchtools._PitchSet import _PitchSet


class NamedChromaticPitchSet(_PitchSet):
    '''.. versionadded:: 2.0

    Abjad model of a named chromatic pitch set::

        abjad> pitchtools.NamedChromaticPitchSet(['bf', 'bqf', "fs'", "g'", 'bqf', "g'"])
        NamedChromaticPitchSet(['bf', 'bqf', "fs'", "g'"])

    Named chromatic pitch sets are immutable.
    '''

    def __new__(klass, pitch_tokens):
        from abjad.tools import notetools
        from abjad.tools import pitchtools
        pitches = []
        for token in pitch_tokens:
            if isinstance(token, notetools.NoteHead):
                pitch = pitchtools.NamedChromaticPitch(token.written_pitch)
                pitches.append(pitch)
            else:
                pitch = pitchtools.NamedChromaticPitch(token)
                pitches.append(pitch)
        return frozenset.__new__(klass, pitches)

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            for element in arg:
                if element not in self:
                    return False
            else:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s([%s])' % (type(self).__name__, self._repr_string)

    def __str__(self):
        return '{%s}' % ' '.join([str(pitch) for pitch in self.named_chromatic_pitches])

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return ', '.join([str(pitch) for pitch in self.pitches])

    @property
    def _repr_string(self):
        return ', '.join([repr(str(pitch)) for pitch in self.named_chromatic_pitches])

    ### PUBLIC ATTRIBUTES ###

    @property
    #def numbers(self):
    def chromatic_pitch_numbers(self):
        return tuple(sorted([pitch.numbered_chromatic_pitch._chromatic_pitch_number for pitch in self]))

    @property
    def duplicate_pitch_classes(self):
        from abjad.tools import pitchtools
        pitch_classes = []
        duplicate_pitch_classes = []
        for pitch in self:
            pitch_class = pitch.numbered_chromatic_pitch_class
            if pitch_class in pitch_classes:
                duplicate_pitch_classes.append(pitch_class)
            pitch_classes.append(pitch_class)
        return pitchtools.NumberedChromaticPitchClassSet(duplicate_pitch_classes)

    @property
    def is_pitch_class_unique(self):
        return len(self) == len(self.numbered_chromatic_pitch_class_set)

    @property
    #def pitches(self):
    def named_chromatic_pitches(self):
        return tuple(sorted(self))

    @property
    #def pitch_class_set(self):
    def numbered_chromatic_pitch_class_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedChromaticPitchClassSet(self)

    @property
    #def pitch_classes(self):
    def numbered_chromatic_pitch_classes(self):
        return tuple([pitch.numbered_chromatic_pitch_class for pitch in self.pitches])

    ### PUBLIC METHODS ###

    # TODO: Implement pitch set (axis) inversion. #

    #def invert(self):
    #    '''Transpose all pcs in self by n.'''
    #    return PCSet([pc.invert() for pc in self])

    def transpose(self, n):
        '''Transpose all pcs in self by n.'''
        from abjad.tools import pitchtools
        interval = pitchtools.MelodicChromaticInterval(n)
        return type(self)([
            pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, interval) for pitch in self])
