from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools.pitchtools.NamedChromaticPitchClassSegment import NamedChromaticPitchClassSegment


class Scale(NamedChromaticPitchClassSegment):
    '''.. versionadded:: 2.0

    Abjad model of diatonic scale.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = (repr('c'), repr('major'))

    ### INITIALIZER ###

    def __new__(klass, *args):
        if len(args) == 1 and isinstance(args[0], contexttools.KeySignatureMark):
            key_signature = args[0]
        elif len(args) == 1 and isinstance(args[0], Scale):
            key_signature = args[0].key_signature
        elif len(args) == 2:
            key_signature = contexttools.KeySignatureMark(*args)
        else:
            raise TypeError
        npcs = [key_signature.tonic]
        for mdi in key_signature.mode.melodic_diatonic_interval_segment[:-1]:
            named_chromatic_pitch_class = npcs[-1] + mdi
            npcs.append(named_chromatic_pitch_class)
        new = tuple.__new__(klass, npcs)
        tuple.__setattr__(new, '_key_signature', key_signature)
        return new

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (self._capital_name, self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _capital_name(self):
        letter = str(self.key_signature.tonic).title()
        mode = self.key_signature.mode.mode_name.title()
        return '%s%s' % (letter, mode)

    ### PUBLIC PROPERTIES ###

    @property
    def diatonic_interval_class_segment(self):
        dics = []
        for left, right in sequencetools.iterate_sequence_pairwise_wrapped(self):
            dic = left - right
            dics.append(dic)
        dicg = pitchtools.InversionEquivalentDiatonicIntervalClassSegment(dics)
        return dicg

    @property
    def dominant(self):
        return self[4]

    @property
    def key_signature(self):
        return self._key_signature

    @property
    def leading_tone(self):
        return self[-1]

    @property
    def mediant(self):
        return self[2]

    @property
    def subdominant(self):
        return self[3]

    @property
    def submediant(self):
        return self[5]

    @property
    def superdominant(self):
        return self[1]

    @property
    def tonic(self):
        return self[0]

    ### PUBLIC METHODS ###

    def create_named_chromatic_pitch_set_in_pitch_range(self, pitch_range):
        if not isinstance(pitch_range, pitchtools.PitchRange):
            pitch_range = pitchtools.PitchRange(float(pitchtools.NamedChromaticPitch(pitch_range[0])), \
                float(pitchtools.NamedChromaticPitch(pitch_range[1])))
        low = pitch_range.start_pitch.octave_number
        high = pitch_range.stop_pitch.octave_number
        pitches = []
        octave = low
        while octave <= high:
            for x in self:
                pitch = pitchtools.NamedChromaticPitch(x, octave)
                if pitch_range.start_pitch <= pitch and \
                    pitch <= pitch_range.stop_pitch:
                    pitches.append(pitch)
            octave += 1
        return pitchtools.NamedChromaticPitchSet(pitches)

    def named_chromatic_pitch_class_to_scale_degree(self, *args):
        from abjad.tools import tonalitytools
        foreign_pitch_class = pitchtools.NamedChromaticPitchClass(*args)
        letter = foreign_pitch_class._diatonic_pitch_class_name
        for i, pc in enumerate(self):
            if pc._diatonic_pitch_class_name == letter:
                native_pitch_class = pc
                scale_degree_index = i
                scale_degree_number = scale_degree_index + 1
                break
        native_pitch = pitchtools.NamedChromaticPitch(native_pitch_class, 4)
        foreign_pitch = pitchtools.NamedChromaticPitch(foreign_pitch_class, 4)
        accidental = foreign_pitch._accidental - native_pitch._accidental
        return tonalitytools.ScaleDegree(accidental, scale_degree_number)

    def scale_degree_to_named_chromatic_pitch_class(self, *args):
        from abjad.tools import tonalitytools
        scale_degree = tonalitytools.ScaleDegree(*args)
        scale_index = scale_degree.number - 1
        pitch_class = self[scale_index]
        pitch_class = pitch_class.apply_accidental(scale_degree._accidental)
        return pitch_class
