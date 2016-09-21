# -*- coding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import systemtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import set_
from abjad.tools.pitchtools.PitchClassSegment import PitchClassSegment


class Scale(PitchClassSegment):
    '''A diatonic scale.

    ::

        >>> scale = tonalanalysistools.Scale('c', 'minor')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_key_signature',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 0:
            key_signature = indicatortools.KeySignature('c', 'major')
        elif len(args) == 1 and isinstance(
            args[0], indicatortools.KeySignature):
            key_signature = args[0]
        elif len(args) == 1 and isinstance(args[0], Scale):
            key_signature = args[0].key_signature
        elif len(args) == 2:
            key_signature = indicatortools.KeySignature(*args)
        else:
            raise TypeError
        npcs = [key_signature.tonic]
        for mdi in key_signature.mode.named_interval_segment[:-1]:
            named_pitch_class = npcs[-1] + mdi
            npcs.append(named_pitch_class)
        PitchClassSegment.__init__(
            self,
            items=npcs,
            item_class=pitchtools.NamedPitchClass,
            )
        self._key_signature = key_signature

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[
                str(self.key_signature.tonic),
                self.key_signature.mode.mode_name,
                ],
            )

    def _set_ascending_named_diatonic_pitches_on_logical_ties_in_expr(
        self, expr):
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        dicg = self.named_interval_class_segment
        length = len(dicg)
        octave_number = 4
        pitch = pitchtools.NamedPitch(self[0], octave_number)
        for i, logical_tie in enumerate(iterate(expr).by_logical_tie()):
            if isinstance(logical_tie[0], scoretools.Note):
                for note in logical_tie:
                    note.written_pitch = pitch
            elif isinstance(logical_tie[0], scoretools.Chord):
                for chord in logical_tie:
                    chord.written_pitches = [pitch]
            else:
                pass
            dic = dicg[i % length]
            ascending_mdi = pitchtools.NamedInterval(dic.quality_string, dic.number)
            pitch += ascending_mdi

    ### PUBLIC METHODS ###

    def create_named_pitch_set_in_pitch_range(self, pitch_range):
        r'''Creates named pitch-set in `pitch_range`.

        Returns pitch-set.
        '''
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
            items=pitches,
            item_class=pitchtools.NamedPitch,
            )

    @classmethod
    def from_selection(class_, selection, item_class=None, name=None):
        r'''Make scale from `selection`.

        Returns new scale.
        '''
        raise NotImplementedError

    def make_notes(self, n, written_duration=None):
        r'''Makes first `n` notes in ascending diatonic scale
        according to `key_signature`.

        Set `written_duration` equal to `written_duration` or ``1/8``:

        ::

            >>> scale = tonalanalysistools.Scale('c', 'major')
            >>> notes = scale.make_notes(8)
            >>> staff = Staff(notes)

        ..  doctest::

            >>> print(format(staff))
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
            >>> time_signature = TimeSignature((5, 4))
            >>> attach(time_signature, staff)

        ..  doctest::

            >>> print(format(staff))
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

        Returns list of notes.
        '''
        written_duration = written_duration or durationtools.Duration(1, 8)
        result = scoretools.make_notes(n * [0], [written_duration])
        self._set_ascending_named_diatonic_pitches_on_logical_ties_in_expr(
            result)
        return result

    def make_score(self):
        r'''Make MIDI playback score from scale:

        ::

            >>> scale = tonalanalysistools.Scale('E', 'major')
            >>> score = scale.make_score()

        ..  doctest::

            >>> print(format(score))
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

        Returns score.
        '''
        ascending_notes = self.make_notes(8, durationtools.Duration(1, 8))
        descending_notes = copy.deepcopy(ascending_notes[:-1])
        descending_notes = list(descending_notes)
        descending_notes.reverse()
        descending_notes = selectiontools.Selection(descending_notes)
        notes = ascending_notes + descending_notes
        notes[-1].written_duration = durationtools.Duration(1, 4)
        staff = scoretools.Staff(notes)
        key_signature = copy.copy(self.key_signature)
        attach(key_signature, staff)
        score = scoretools.Score([staff])
        set_(score).tempo_wholes_per_minute = schemetools.SchemeMoment(30)
        return score

    def named_pitch_class_to_scale_degree(self, *args):
        r'''Changes named pitch-class to scale degree.

        Returns scale degree.
        '''
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
        r'''Changes scale degree to named pitch-class.

        ::

            >>> scale = tonalanalysistools.Scale('c', 'major')
            >>> scale_degree = tonalanalysistools.ScaleDegree('flat', 5)
            >>> scale.scale_degree_to_named_pitch_class(scale_degree)
            NamedPitchClass('gf')

        ::

            >>> scale_degree = tonalanalysistools.ScaleDegree('flat', 9)
            >>> scale.scale_degree_to_named_pitch_class(scale_degree)
            NamedPitchClass('df')

        Returns named pitch-class.
        '''
        from abjad.tools import tonalanalysistools
        scale_degree = tonalanalysistools.ScaleDegree(*args)
        scale_index = (scale_degree.number - 1) % 7
        pitch_class = self[scale_index]
        pitch_class = pitch_class.apply_accidental(scale_degree.accidental)
        return pitch_class

    def voice_scale_degrees_in_open_position(self, scale_degrees):
        r'''Voice `scale_degrees` in open position:

        ::

            >>> scale = tonalanalysistools.Scale('c', 'major')
            >>> scale_degrees = [1, 3, ('flat', 5), 7, ('sharp', 9)]
            >>> pitches = scale.voice_scale_degrees_in_open_position(
            ...     scale_degrees)
            >>> pitches
            PitchSegment(["c'", "e'", "gf'", "b'", "ds''"])

        Return pitch segment.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import tonalanalysistools
        scale_degrees = [tonalanalysistools.ScaleDegree(x)
            for x in scale_degrees]
        pitch_classes = [self.scale_degree_to_named_pitch_class(x)
            for x in scale_degrees]
        pitches = [pitchtools.NamedPitch(pitch_classes[0])]
        for pitch_class in pitch_classes[1:]:
            pitch = pitchtools.NamedPitch(pitch_class)
            while pitch < pitches[-1]:
                pitch += 12
            pitches.append(pitch)
        pitches = pitchtools.PitchSegment(pitches)
        return pitches

    ### PRIVATE PROPERTIES ###

    @property
    def _capital_name(self):
        letter = str(self.key_signature.tonic).title()
        mode = self.key_signature.mode.mode_name.title()
        return '{}{}'.format(letter, mode)

    ### PUBLIC PROPERTIES ###

    @property
    def dominant(self):
        r'''Dominant of scale.

        Return pitch-class.
        '''
        return self[4]

    @property
    def key_signature(self):
        r'''Key signature of scale.

        Returns key signature.
        '''
        return self._key_signature

    @property
    def leading_tone(self):
        r'''Leading tone of scale.

        Returns pitch-class.
        '''
        return self[-1]

    @property
    def mediant(self):
        r'''Mediant of scale.

        Returns pitch-class.
        '''
        return self[2]

    @property
    def named_interval_class_segment(self):
        r'''Named interval class segment of scale.

        Returns interval-class segment.
        '''
        dics = []
        for left, right in \
            sequencetools.iterate_sequence_nwise(self, wrapped=True):
            dic = left - right
            dics.append(dic)
        dicg = pitchtools.IntervalClassSegment(
            items=dics,
            item_class=pitchtools.NamedInversionEquivalentIntervalClass,
            )
        return dicg

    @property
    def subdominant(self):
        r'''Subdominant of scale.

        Returns pitch-class.
        '''
        return self[3]

    @property
    def submediant(self):
        r'''Submediate of scale.

        Returns pitch-class.
        '''
        return self[5]

    @property
    def superdominant(self):
        r'''Superdominant of scale.

        Returns pitch-class.
        '''
        return self[1]

    @property
    def tonic(self):
        r'''Tonic of scale.

        Returns pitch-class.
        '''
        return self[0]
