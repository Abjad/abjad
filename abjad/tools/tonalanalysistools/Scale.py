import copy
from abjad.tools.pitchtools.PitchClassSegment import PitchClassSegment


class Scale(PitchClassSegment):
    '''Scale.

    ..  container:: example

        Initializes from pair:

        >>> abjad.tonalanalysistools.Scale(('c', 'minor'))
        Scale("c d ef f g af bf")

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_key_signature',
        )

    ### INITIALIZER ###

    def __init__(self, key_signature=None):
        import abjad
        if key_signature is None:
            key_signature = abjad.KeySignature('c', 'major')
        elif isinstance(key_signature, tuple):
            key_signature = abjad.KeySignature(*key_signature)
        elif isinstance(key_signature, type(self)):
            key_signature = key_signature.key_signature
        if not isinstance(key_signature, abjad.KeySignature):
            raise Exception(key_signature)
        npcs = [key_signature.tonic]
        for mdi in key_signature.mode.named_interval_segment[:-1]:
            named_pitch_class = npcs[-1] + mdi
            npcs.append(named_pitch_class)
        PitchClassSegment.__init__(
            self,
            items=npcs,
            item_class=abjad.NamedPitchClass,
            )
        self._key_signature = key_signature

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets item in scale.

        Returns pitch-class segment.
        '''
        segment = PitchClassSegment(self)
        return segment.__getitem__(argument)

    ### PRIVATE PROPERTIES ###

    @property
    def _capital_name(self):
        letter = str(self.key_signature.tonic).title()
        mode = self.key_signature.mode.mode_name.title()
        return '{}{}'.format(letter, mode)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[
                str(self.key_signature.tonic),
                self.key_signature.mode.mode_name,
                ],
            )

    def _set_ascending_named_diatonic_pitches_on_logical_ties(
        self, argument):
        import abjad
        dicg = self.named_interval_class_segment
        length = len(dicg)
        octave_number = 4
        pitch = abjad.NamedPitch((self[0].name, octave_number))
        for i, logical_tie in enumerate(abjad.iterate(argument).logical_ties()):
            if isinstance(logical_tie[0], abjad.Note):
                for note in logical_tie:
                    note.written_pitch = pitch
            elif isinstance(logical_tie[0], abjad.Chord):
                for chord in logical_tie:
                    chord.written_pitches = [pitch]
            else:
                pass
            dic = dicg[i % length]
            ascending_mdi = abjad.NamedInterval.from_quality_and_number(
                dic.quality_string,
                dic.number,
                )
            pitch += ascending_mdi

    ### PUBLIC PROPERTIES ###

    @property
    def dominant(self):
        r'''Gets dominant.

        ..  container:: example

            >>> abjad.tonalanalysistools.Scale(('c', 'minor')).dominant
            NamedPitchClass('g')

        Return pitch-class.
        '''
        return self[4]

    @property
    def key_signature(self):
        r'''Gets key signature.

        ..  container:: example

            >>> abjad.tonalanalysistools.Scale(('c', 'minor')).key_signature
            KeySignature(NamedPitchClass('c'), Mode('minor'))

        Returns key signature.
        '''
        return self._key_signature

    @property
    def leading_tone(self):
        r'''Gets leading tone.

        ..  container:: example

            >>> abjad.tonalanalysistools.Scale(('c', 'minor')).leading_tone
            NamedPitchClass('bf')

        Returns pitch-class.
        '''
        return self[-1]

    @property
    def mediant(self):
        r'''Gets mediant.

        ..  container:: example

            >>> abjad.tonalanalysistools.Scale(('c', 'minor')).mediant
            NamedPitchClass('ef')

        Returns pitch-class.
        '''
        return self[2]

    @property
    def named_interval_class_segment(self):
        r'''Gets named interval class segment.

        ..  container:: example

            >>> scale = abjad.tonalanalysistools.Scale(('c', 'minor'))
            >>> str(scale.named_interval_class_segment)
            '<+M2, +m2, +M2, +M2, +m2, +M2, +M2>'

            >>> scale = abjad.tonalanalysistools.Scale(('d', 'dorian'))
            >>> str(scale.named_interval_class_segment)
            '<+M2, +m2, +M2, +M2, +M2, +m2, +M2>'

        Returns interval-class segment.
        '''
        import abjad
        dics = []
        for left, right in abjad.sequence(self).nwise(wrapped=True):
            dic = left - right
            dics.append(dic)
        dicg = abjad.IntervalClassSegment(
            items=dics,
            item_class=abjad.NamedInversionEquivalentIntervalClass,
            )
        return dicg

    @property
    def subdominant(self):
        r'''Gets subdominant.

        ..  container:: example

            >>> abjad.tonalanalysistools.Scale(('c', 'minor')).subdominant
            NamedPitchClass('f')

        Returns pitch-class.
        '''
        return self[3]

    @property
    def submediant(self):
        r'''Submediate of scale.

        ..  container:: example

            >>> abjad.tonalanalysistools.Scale(('c', 'minor')).submediant
            NamedPitchClass('af')

        Returns pitch-class.
        '''
        return self[5]

    @property
    def superdominant(self):
        r'''Gets superdominant.

        ..  container:: example

            >>> abjad.tonalanalysistools.Scale(('c', 'minor')).superdominant
            NamedPitchClass('d')

        Returns pitch-class.
        '''
        return self[1]

    @property
    def tonic(self):
        r'''Gets tonic.

        ..  container:: example

            >>> abjad.tonalanalysistools.Scale(('c', 'minor')).tonic
            NamedPitchClass('c')

        Returns pitch-class.
        '''
        return self[0]

    ### PUBLIC METHODS ###

    def create_named_pitch_set_in_pitch_range(self, pitch_range):
        r'''Creates named pitch-set in `pitch_range`.

        Returns pitch-set.
        '''
        import abjad
        if not isinstance(pitch_range, abjad.PitchRange):
            pitch_range = abjad.PitchRange(
                float(abjad.NamedPitch(pitch_range[0])),
                float(abjad.NamedPitch(pitch_range[1])))
        low = pitch_range.start_pitch.octave.number
        high = pitch_range.stop_pitch.octave.number
        pitches = []
        octave = low
        while octave <= high:
            for x in self:
                pitch = abjad.NamedPitch((x.name, octave))
                if (pitch_range.start_pitch <= pitch and
                    pitch <= pitch_range.stop_pitch):
                    pitches.append(pitch)
            octave += 1
        return abjad.PitchSet(
            items=pitches,
            item_class=abjad.NamedPitch,
            )

    @classmethod
    def from_selection(class_, selection, item_class=None, name=None):
        r'''Makes scale from `selection`.

        Returns new scale.
        '''
        raise NotImplementedError

    def make_notes(self, n, written_duration=(1, 8)):
        r'''Makes first `n` notes in ascending scale.

        ..  container:: example

            >>> scale = abjad.tonalanalysistools.Scale(('c', 'major'))
            >>> notes = scale.make_notes(8)
            >>> staff = abjad.Staff(notes)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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

        Returns selection of notes.
        '''
        import abjad
        written_duration = written_duration or abjad.Duration(1, 8)
        maker = abjad.NoteMaker()
        result = maker(n * [0], [written_duration])
        self._set_ascending_named_diatonic_pitches_on_logical_ties(result)
        return result

    def make_score(self):
        r'''Makes MIDI playback score from scale.

        ..  container:: example

            >>> scale = abjad.tonalanalysistools.Scale(('E', 'major'))
            >>> score = scale.make_score()
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
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

        Returns score.
        '''
        import abjad
        ascending_notes = self.make_notes(8, abjad.Duration(1, 8))
        descending_notes = copy.deepcopy(ascending_notes[:-1])
        descending_notes = list(descending_notes)
        descending_notes.reverse()
        descending_notes = abjad.select(descending_notes)
        notes = ascending_notes + descending_notes
        notes[-1].written_duration = abjad.Duration(1, 4)
        staff = abjad.Staff(notes)
        key_signature = copy.copy(self.key_signature)
        abjad.attach(key_signature, staff[0])
        score = abjad.Score([staff])
        abjad.setting(score).tempo_wholes_per_minute = abjad.SchemeMoment(30)
        return score

    def named_pitch_class_to_scale_degree(self, pitch_class):
        r'''Changes named `pitch_class` to scale degree.

        ..  container:: example

            >>> scale = abjad.tonalanalysistools.Scale(('c', 'major'))
            >>> scale.named_pitch_class_to_scale_degree('c')
            ScaleDegree('1')
            >>> scale.named_pitch_class_to_scale_degree('d')
            ScaleDegree('2')
            >>> scale.named_pitch_class_to_scale_degree('e')
            ScaleDegree('3')
            >>> scale.named_pitch_class_to_scale_degree('f')
            ScaleDegree('4')
            >>> scale.named_pitch_class_to_scale_degree('g')
            ScaleDegree('5')
            >>> scale.named_pitch_class_to_scale_degree('a')
            ScaleDegree('6')
            >>> scale.named_pitch_class_to_scale_degree('b')
            ScaleDegree('7')

            >>> scale.named_pitch_class_to_scale_degree('df')
            ScaleDegree('b2')

        Returns scale degree.
        '''
        import abjad
        foreign_pitch_class = abjad.NamedPitchClass(pitch_class)
        letter = foreign_pitch_class._get_diatonic_pitch_class_name()
        for i, pc in enumerate(self):
            if pc._get_diatonic_pitch_class_name() == letter:
                native_pitch_class = pc
                scale_degree_index = i
                number = scale_degree_index + 1
                break
        native_pitch = abjad.NamedPitch((native_pitch_class.name, 4))
        foreign_pitch = abjad.NamedPitch((foreign_pitch_class.name, 4))
        accidental = foreign_pitch.accidental - native_pitch.accidental
        class_ = abjad.tonalanalysistools.ScaleDegree
        scale_degree = class_.from_accidental_and_number(accidental, number)
        return scale_degree

    def scale_degree_to_named_pitch_class(self, scale_degree):
        r'''Changes scale degree to named pitch-class.

        ..  container:: example

            >>> scale = abjad.tonalanalysistools.Scale(('c', 'major'))
            >>> scale.scale_degree_to_named_pitch_class('1')
            NamedPitchClass('c')
            >>> scale.scale_degree_to_named_pitch_class('2')
            NamedPitchClass('d')
            >>> scale.scale_degree_to_named_pitch_class('3')
            NamedPitchClass('e')
            >>> scale.scale_degree_to_named_pitch_class('4')
            NamedPitchClass('f')
            >>> scale.scale_degree_to_named_pitch_class('5')
            NamedPitchClass('g')
            >>> scale.scale_degree_to_named_pitch_class('6')
            NamedPitchClass('a')
            >>> scale.scale_degree_to_named_pitch_class('7')
            NamedPitchClass('b')

            >>> scale.scale_degree_to_named_pitch_class('b2')
            NamedPitchClass('df')

        Returns named pitch-class.
        '''
        import abjad
        scale_degree = abjad.tonalanalysistools.ScaleDegree(scale_degree)
        scale_index = (scale_degree.number - 1) % 7
        pitch_class = self[scale_index]
        pitch_class = scale_degree.accidental(pitch_class)
        return pitch_class

    def voice_scale_degrees_in_open_position(self, scale_degrees):
        r'''Voices `scale_degrees` in open position.

        ..  container:: example

            >>> scale = abjad.tonalanalysistools.Scale(('c', 'major'))
            >>> scale_degrees = [1, 3, 'b5', 7, '#9']
            >>> segment = scale.voice_scale_degrees_in_open_position(
            ...     scale_degrees)
            >>> segment
            PitchSegment("c' e' gf' b' ds''")

        Return pitch segment.
        '''
        import abjad
        from abjad.tools import tonalanalysistools
        scale_degrees = [tonalanalysistools.ScaleDegree(x)
            for x in scale_degrees]
        pitch_classes = [self.scale_degree_to_named_pitch_class(x)
            for x in scale_degrees]
        pitches = [abjad.NamedPitch(pitch_classes[0])]
        for pitch_class in pitch_classes[1:]:
            pitch = abjad.NamedPitch(pitch_class)
            while pitch < pitches[-1]:
                pitch += 12
            pitches.append(pitch)
        pitches = abjad.PitchSegment(pitches)
        return pitches
