# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.PitchSet import PitchSet


class NamedPitchSet(PitchSet):
    '''Abjad model of a named chromatic pitch set:

    ::

        >>> pitchtools.NamedPitchSet(
        ...     ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"])
        NamedPitchSet(['bf', "fs'", 'bqf', "g'"])

    Named chromatic pitch sets are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools 
        PitchSet.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NamedPitch,
            name=name,
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s([%s])' % (self._class_name, self._repr_string)

    def __str__(self):
        return '{%s}' % ' '.join([str(pitch) 
            for pitch in self.named_chromatic_pitches])

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join(str(pitch) for pitch in self.pitches)

    @property
    def _repr_string(self):
        return ', '.join(repr(str(pitch)) for pitch in self)

    ### PUBLIC PROPERTIES ###

    @property
    #def numbers(self):
    def chromatic_pitch_numbers(self):
        return tuple(sorted([
            pitch.numbered_chromatic_pitch._chromatic_pitch_number 
            for pitch in self]))

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
        return pitchtools.PitchClassSet(
            duplicate_pitch_classes,
            item_class=pitchtools.NumberedPitchClass,
            )

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
        return pitchtools.PitchClassSet(
            self, 
            item_class=pitchtools.NumberedPitchClass,
            )

    @property
    #def pitch_classes(self):
    def numbered_chromatic_pitch_classes(self):
        return tuple([pitch.numbered_chromatic_pitch_class 
            for pitch in self.pitches])

    ### PUBLIC METHODS ###

    # TODO: Implement pitch set (axis) inversion.

    #def invert(self):
    #    r'''Transpose all pcs in self by n.'''
    #    return PCSet([pc.invert() for pc in self])

    def transpose(self, n):
        r'''Transpose all pcs in self by n.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.NumberedMelodicInterval(n)
        return type(self)([
            pitchtools.transpose_pitch_carrier_by_melodic_interval(
            pitch, interval) for pitch in self])
