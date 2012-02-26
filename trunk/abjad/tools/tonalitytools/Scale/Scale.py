from abjad.tools.contexttools.KeySignatureMark import KeySignatureMark
from abjad.tools.pitchtools.HarmonicDiatonicIntervalSegment import HarmonicDiatonicIntervalSegment
from abjad.tools.pitchtools.MelodicDiatonicIntervalSegment import MelodicDiatonicIntervalSegment
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.NamedChromaticPitchClass import NamedChromaticPitchClass
from abjad.tools.pitchtools.NamedChromaticPitchClassSegment import NamedChromaticPitchClassSegment
from abjad.tools.pitchtools.NamedChromaticPitchSet import NamedChromaticPitchSet
from abjad.tools.pitchtools.PitchRange import PitchRange
from abjad.tools.tonalitytools.ScaleDegree import ScaleDegree


class Scale(NamedChromaticPitchClassSegment):
    '''.. versionadded:: 2.0

    Abjad model of diatonic scale.
    '''

    def __new__(klass, *args):
        if len(args) == 1 and isinstance(args[0], KeySignatureMark):
            key_signature = args[0]
        elif len(args) == 1 and isinstance(args[0], Scale):
            key_signature = args[0].key_signature
        elif len(args) == 2:
            key_signature = KeySignatureMark(*args)
        else:
            raise TypeError
        npcs = [key_signature.tonic]
        for mdi in key_signature.mode.melodic_diatonic_interval_segment[:-1]:
            named_chromatic_pitch_class = npcs[-1] + mdi
            npcs.append(named_chromatic_pitch_class)
        new = tuple.__new__(klass, npcs)
        tuple.__setattr__(new, '_key_signature', key_signature)
        return new

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (self._capital_name, self._format_string)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _capital_name(self):
        letter = str(self.key_signature.tonic).title()
        mode = self.key_signature.mode.mode_name.title()
        return '%s%s' % (letter, mode)

    ### PUBLIC ATTRIBUTES ###

    @property
    def diatonic_interval_class_segment(self):
        from abjad.tools import sequencetools
        from abjad.tools import pitchtools
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
        if not isinstance(pitch_range, PitchRange):
            pitch_range = PitchRange(float(NamedChromaticPitch(pitch_range[0])), \
                float(NamedChromaticPitch(pitch_range[1])))
        low = pitch_range.start_pitch.octave_number
        high = pitch_range.stop_pitch.octave_number
        pitches = [ ]
        octave = low
        while octave <= high:
            for x in self:
                pitch = NamedChromaticPitch(x, octave)
                if pitch_range.start_pitch <= pitch and \
                    pitch <= pitch_range.stop_pitch:
                    pitches.append(pitch)
            octave += 1
        return NamedChromaticPitchSet(pitches)

    def named_chromatic_pitch_class_to_scale_degree(self, *args):
        foreign_pitch_class = NamedChromaticPitchClass(*args)
        letter = foreign_pitch_class._diatonic_pitch_class_name
        for i, pc in enumerate(self):
            if pc._diatonic_pitch_class_name == letter:
                native_pitch_class = pc
                scale_degree_index = i
                scale_degree_number = scale_degree_index + 1
                break
        native_pitch = NamedChromaticPitch(native_pitch_class, 4)
        foreign_pitch = NamedChromaticPitch(foreign_pitch_class, 4)
        accidental = foreign_pitch._accidental - native_pitch._accidental
        return ScaleDegree(accidental, scale_degree_number)

    def scale_degree_to_named_chromatic_pitch_class(self, *args):
        scale_degree = ScaleDegree(*args)
        scale_index = scale_degree.number - 1
        pitch_class = self[scale_index]
        pitch_class = pitch_class.apply_accidental(scale_degree._accidental)
        return pitch_class
