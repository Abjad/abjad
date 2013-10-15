# -*- encoding: utf-8 -*-
import copy
from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import notetools
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import stafftools
from abjad.tools.pitchtools.PitchClassSegment \
    import PitchClassSegment


class Scale(PitchClassSegment):
    '''Abjad model of diatonic scale.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('c'),
        repr('major',)
        )

    __slots__ = (
        '_key_signature',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1 and isinstance(
            args[0], contexttools.KeySignatureMark):
            key_signature = args[0]
        elif len(args) == 1 and isinstance(args[0], Scale):
            key_signature = args[0].key_signature
        elif len(args) == 2:
            key_signature = contexttools.KeySignatureMark(*args)
        else:
            raise TypeError
        npcs = [key_signature.tonic]
        for mdi in key_signature.mode.melodic_diatonic_interval_segment[:-1]:
            named_pitch_class = npcs[-1] + mdi
            npcs.append(named_pitch_class)
        PitchClassSegment.__init__(
            self, 
            tokens=npcs,
            item_class=pitchtools.NamedPitchClass,
            )
        self._key_signature = key_signature

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(self._capital_name, self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _capital_name(self):
        letter = str(self.key_signature.tonic).title()
        mode = self.key_signature.mode.mode_name.title()
        return '{}{}'.format(letter, mode)

    ### PRIVATE METHODS ###

    def _set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(self, expr):
        from abjad.tools import chordtools
        from abjad.tools import iterationtools
        from abjad.tools import notetools
        from abjad.tools import pitchtools
        from abjad.tools import tonalanalysistools

        dicg = self.diatonic_interval_class_segment
        length = len(dicg)

        octave_number = 4
        pitch = pitchtools.NamedPitch(self[0], octave_number)

        for i, tie_chain in enumerate(iterationtools.iterate_tie_chains_in_expr(expr)):
            if isinstance(tie_chain[0], notetools.Note):
                for note in tie_chain:
                    note.written_pitch = pitch
            elif isinstance(tie_chain[0], chordtools.Chord):
                for chord in tie_chain:
                    chord.written_pitches = [pitch]
            else:
                pass
            dic = dicg[i % length]
            ascending_mdi = pitchtools.NamedInterval(dic.quality_string, dic.number)
            pitch += ascending_mdi

    ### PUBLIC PROPERTIES ###

    @property
    def diatonic_interval_class_segment(self):
        dics = []
        for left, right in \
            sequencetools.iterate_sequence_pairwise_wrapped(self):
            dic = left - right
            dics.append(dic)
        dicg = pitchtools.IntervalClassSegment(
            tokens=dics,
            item_class=pitchtools.NamedInversionEquivalentIntervalClass,
            )
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

    def create_named_pitch_set_in_pitch_range(self, pitch_range):
        if not isinstance(pitch_range, pitchtools.PitchRange):
            pitch_range = pitchtools.PitchRange(
                float(pitchtools.NamedPitch(pitch_range[0])),
                float(pitchtools.NamedPitch(pitch_range[1])))
        low = pitch_range.start_pitch.octave_number
        high = pitch_range.stop_pitch.octave_number
        pitches = []
        octave = low
        while octave <= high:
            for x in self:
                pitch = pitchtools.NamedPitch(x, octave)
                if pitch_range.start_pitch <= pitch and \
                    pitch <= pitch_range.stop_pitch:
                    pitches.append(pitch)
            octave += 1
        return pitchtools.PitchSet(
            tokens=pitches,
            item_class=pitchtools.NamedPitch,
            )

    @classmethod
    def from_selection(cls, selection, item_class=None, name=None):
        raise NotImplementedError

    def make_notes(self, n, written_duration=None):
        r'''Make first `n` notes in ascending diatonic scale.
        according to `key_signature`.

        Set `written_duration` equal to `written_duration` or ``1/8``:

        ::

            >>> scale = tonalanalysistools.Scale('c', 'major')
            >>> notes = scale.make_notes(8)
            >>> staff = Staff(notes)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Allow nonassignable `written_duration`:

        ::

            >>> notes = scale.make_notes(4, Duration(5, 16))
            >>> staff = Staff(notes)
            >>> time_signature = contexttools.TimeSignatureMark((5, 4))(staff)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 5/4
                c'4 ~
                c'16
                d'4 ~
                d'16
                e'4 ~
                e'16
                f'4 ~
                f'16
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Return list of notes.
        '''
        written_duration = written_duration or durationtools.Duration(1, 8)
        result = notetools.make_notes(n * [0], [written_duration])
        self._set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
            result)
        return result

    def make_score(self):
        r'''Make MIDI playback score from scale:

        ::

            >>> scale = tonalanalysistools.Scale('E', 'major')
            >>> score = scale.make_score()

        ..  doctest::

            >>> f(score)
            \new Score \with {
                tempoWholesPerMinute = #(ly:make-moment 30 1)
            } <<
                \new Staff {
                    \key e \major
                    e'8
                    fs'8
                    gs'8
                    a'8
                    b'8
                    cs''8
                    ds''8
                    e''8
                    ds''8
                    cs''8
                    b'8
                    a'8
                    gs'8
                    fs'8
                    e'4
                }
            >>

        ::

            >>> show(score) # doctest: +SKIP

        Return score.
        '''
        ascending_notes = self.make_notes(8, durationtools.Duration(1, 8))
        descending_notes = copy.deepcopy(ascending_notes[:-1])
        descending_notes = list(descending_notes)
        descending_notes.reverse()
        descending_notes = selectiontools.Selection(descending_notes)
        notes = ascending_notes + descending_notes
        notes[-1].written_duration = durationtools.Duration(1, 4)
        staff = stafftools.Staff(notes)
        key_signature = copy.copy(self.key_signature)
        key_signature.attach(staff)
        score = scoretools.Score([staff])
        score.set.tempo_wholes_per_minute = schemetools.SchemeMoment(30)
        return score

    def named_pitch_class_to_scale_degree(self, *args):
        from abjad.tools import tonalanalysistools
        foreign_pitch_class = pitchtools.NamedPitchClass(*args)
        letter = foreign_pitch_class.diatonic_pitch_class_name
        for i, pc in enumerate(self):
            if pc.diatonic_pitch_class_name == letter:
                native_pitch_class = pc
                scale_degree_index = i
                scale_degree_number = scale_degree_index + 1
                break
        native_pitch = pitchtools.NamedPitch(native_pitch_class, 4)
        foreign_pitch = pitchtools.NamedPitch(foreign_pitch_class, 4)
        accidental = foreign_pitch.accidental - native_pitch.accidental
        return tonalanalysistools.ScaleDegree(accidental, scale_degree_number)

    def scale_degree_to_named_pitch_class(self, *args):
        from abjad.tools import tonalanalysistools
        scale_degree = tonalanalysistools.ScaleDegree(*args)
        scale_index = scale_degree.number - 1
        pitch_class = self[scale_index]
        pitch_class = pitch_class.apply_accidental(scale_degree.accidental)
        return pitch_class
