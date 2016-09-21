# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools.topleveltools import iterate


class TonalAnalysisAgent(abctools.AbjadObject):
    r'''A tonal analysis interface.

    ..  container:: example

        **Example 1.** Interface to conjunct selection:

            >>> staff = Staff("c'4 d' e' f'")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

        ::

            >>> selection_1 = tonalanalysistools.select(staff[:])

    ..  container:: example

        **Example 2.** Interface to disjunct selection:

            >>> staff = Staff("c'4 d' e' f'")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

        ::

            >>> selection_2 = tonalanalysistools.select(staff[:1] + staff[-1:])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        from abjad.tools import selectiontools
        if not isinstance(client, selectiontools.Selection):
            client = selectiontools.Selection(client)
        self._client = client

    ### PRIVATE METHODS ###

    @staticmethod
    def _analyze_chord(expr):
        from abjad.tools import tonalanalysistools
        pitches = pitchtools.PitchSegment.from_selection(expr)
        npcset = pitchtools.PitchClassSet(
            pitches,
            item_class=pitchtools.NamedPitchClass,
            )
        ordered_npcs = []
        letters = ('c', 'e', 'g', 'b', 'd', 'f', 'a')
        for letter in letters:
            for npc in npcset:
                if npc.diatonic_pitch_class_name == letter:
                    ordered_npcs.append(npc)
        ordered_npcs = pitchtools.PitchClassSegment(
            ordered_npcs, item_class=pitchtools.NamedPitchClass)
        for x in range(len(ordered_npcs)):
            ordered_npcs = ordered_npcs.rotate(1)
            segment = \
                pitchtools.IntervalClassSegment(
                    items=mathtools.difference_series(ordered_npcs),
                    item_class=pitchtools.NamedInversionEquivalentIntervalClass,
                    )
            if segment.is_tertian:
                break
        else:
            return None
        root = ordered_npcs[0]
        class_ = tonalanalysistools.RootlessChordClass
        rootless_chord_class = class_.from_interval_class_segment(segment)
        bass = min(pitches).named_pitch_class
        inversion = ordered_npcs.index(bass)
        return tonalanalysistools.RootedChordClass(
            root,
            rootless_chord_class.quality_string,
            rootless_chord_class.extent,
            inversion,
            )

    @staticmethod
    def _analyze_incomplete_chord(expr):
        from abjad.tools import tonalanalysistools
        pitches = pitchtools.PitchSegment.from_selection(expr)
        npcset = pitchtools.PitchClassSet(
            pitches, item_class=pitchtools.NamedPitchClass)
        dicv = pitchtools.IntervalClassVector(
            items=npcset,
            item_class=pitchtools.NamedInversionEquivalentIntervalClass,
            )
        # TODO: eliminate code duplication #
        if dicv == TonalAnalysisAgent._make_dicv('c', 'ef'):
            model_npcs = ['c', 'ef']
            quality, extent = 'minor', 'triad'
        elif dicv == TonalAnalysisAgent._make_dicv('c', 'e'):
            model_npcs = ['c', 'e']
            quality, extent = 'major', 'triad'
        elif dicv == TonalAnalysisAgent._make_dicv('c', 'ef', 'bff'):
            model_npcs = ['c', 'ef', 'bff']
            quality, extent = 'diminished', 'seventh'
        elif dicv == TonalAnalysisAgent._make_dicv('c', 'ef', 'bf'):
            model_npcs = ['c', 'ef', 'bf']
            quality, extent = 'minor', 'seventh'
        elif dicv == TonalAnalysisAgent._make_dicv('c', 'e', 'bf'):
            model_npcs = ['c', 'e', 'bf']
            quality, extent = 'dominant', 'seventh'
        elif dicv == TonalAnalysisAgent._make_dicv('c', 'e', 'b'):
            model_npcs = ['c', 'e', 'b']
            quality, extent = 'major', 'seventh'
        else:
            message = 'can not identify incomplete tertian chord.'
            raise ValueError(message)
        bass = min(pitches).named_pitch_class
        try:
            npcseg = npcset.order_by(
                pitchtools.PitchClassSegment(
                    model_npcs,
                    item_class=pitchtools.NamedPitchClass,
                    ))
        except ValueError:
            message = 'can not identify incomplete tertian chord.'
            raise ValueError(message)
        inversion = npcseg.index(bass)
        root = npcseg[0]
        return tonalanalysistools.RootedChordClass(
            root,
            quality,
            extent,
            inversion,
            )

    @staticmethod
    def _analyze_incomplete_tonal_function(expr, key_signature):
        from abjad.tools import tonalanalysistools
        if isinstance(expr, tonalanalysistools.RootedChordClass):
            chord_class = expr
        else:
            selection = tonalanalysistools.select(expr)
            chord_classes = selection.analyze_incomplete_chords()
            assert len(chord_classes) == 1
            chord_class = chord_classes[0]
        root = chord_class.root
        scale = tonalanalysistools.Scale(key_signature)
        scale_degree = scale.named_pitch_class_to_scale_degree(root)
        quality = chord_class.chord_quality.quality_string
        extent = chord_class.extent
        inversion = chord_class.inversion
        return tonalanalysistools.RomanNumeral(
            scale_degree,
            quality,
            extent,
            inversion,
            )

    @staticmethod
    def _analyze_tonal_function(expr, key_signature):
        from abjad.tools import tonalanalysistools
        if isinstance(expr, tonalanalysistools.RootedChordClass):
            chord_class = expr
        else:
            selection = tonalanalysistools.select(expr)
            chord_classes = selection.analyze_chords()
            assert len(chord_classes) == 1
            chord_class = chord_classes[0]
        if chord_class is None:
            return None
        root = chord_class.root
        scale = tonalanalysistools.Scale(key_signature)
        scale_degree = scale.named_pitch_class_to_scale_degree(root)
        quality = chord_class.chord_quality.quality_string
        extent = chord_class.extent
        inversion = chord_class.inversion
        return tonalanalysistools.RomanNumeral(
            scale_degree,
            quality,
            extent,
            inversion,
            )

    @staticmethod
    def _is_neighbor_note(note):
        from abjad.tools import scoretools
        from abjad.tools import tonalanalysistools
        if not isinstance(note, scoretools.Note):
            message = 'must be note: {!r}.'
            message = message.format(note)
            raise TypeError(message)
        previous_note = note._get_in_my_logical_voice(
            -1, prototype=scoretools.Note)
        next_note = note._get_in_my_logical_voice(
            1, prototype=scoretools.Note)
        if previous_note is None:
            return False
        if next_note is None:
            return False
        notes = [previous_note, note, next_note]
        selection = tonalanalysistools.select(notes)
        preceding_interval = note.written_pitch - previous_note.written_pitch
        preceding_interval_direction = \
            mathtools.sign(preceding_interval.direction_number)
        following_interval = next_note.written_pitch - note.written_pitch
        following_interval_direction = \
            mathtools.sign(following_interval.direction_number)
        if selection.are_stepwise_notes():
            if preceding_interval_direction != following_interval_direction:
                return True
        return False

    @staticmethod
    def _is_passing_tone(note):
        from abjad.tools import scoretools
        from abjad.tools import tonalanalysistools
        if not isinstance(note, scoretools.Note):
            message = 'must be note: {!r}.'
            message = message.format(note)
            raise TypeError(message)
        previous_note = note._get_in_my_logical_voice(
            -1, prototype=scoretools.Note)
        next_note = note._get_in_my_logical_voice(
            1, prototype=scoretools.Note)
        if previous_note is None or next_note is None:
            return False
        notes = [previous_note, note, next_note]
        selection = tonalanalysistools.select(notes)
        return selection.are_scalar_notes()

    @staticmethod
    def _make_dicv(*named_pitch_classes):
        pitch_set = pitchtools.PitchSet(named_pitch_classes)
        return pitchtools.IntervalClassVector(
            items=pitch_set,
            item_class=pitchtools.NamedInversionEquivalentIntervalClass,
            )

    ### PUBLIC METHODS ###

    def analyze_chords(self):
        r'''Analyzes chords in selection.

        ..  container:: example

            ::

                >>> chord = Chord([7, 10, 12, 16], (1, 4))
                >>> tonalanalysistools.select(chord).analyze_chords()
                [CDominantSeventhInSecondInversion]

        Returns none when no tonal chord is understood.

        Returns list with elements each equal to chord class or none.
        '''
        result = []
        for component in self._client:
            chord_class = self._analyze_chord(component)
            result.append(chord_class)
        return result

    def analyze_incomplete_chords(self):
        r'''Analyzes incomplete chords in selection.

        ..  container:: example

            ::

                >>> chord = Chord("<g' b'>4")
                >>> tonalanalysistools.select(chord).analyze_incomplete_chords()
                [GMajorTriadInRootPosition]

        ..  container:: example

            ::

                >>> chord = Chord("<fs g b>4")
                >>> tonalanalysistools.select(chord).analyze_incomplete_chords()
                [GMajorSeventhInSecondInversion]

        Raises tonal harmony error when chord in selection can not analyze.

        Returns list with elements each equal to chord class or none.
        '''
        result = []
        for component in self._client:
            chord_class = self._analyze_incomplete_chord(component)
            result.append(chord_class)
        return result

    def analyze_incomplete_tonal_functions(self, key_signature):
        r'''Analyzes incomplete tonal functions of chords in selection
        according to `key_signature`.

        ..  container:: example

            ::

                >>> chord = Chord("<c' e'>4")
                >>> key_signature = KeySignature('g', 'major')
                >>> selection = tonalanalysistools.select(chord)
                >>> selection.analyze_incomplete_tonal_functions(key_signature)
                [IVMajorTriadInRootPosition]

        Raises tonal harmony error when chord in selection can not analyze.

        Returns list with elements each equal to tonal function or none.
        '''
        result = []
        for component in self._client:
            tonal_function = self._analyze_incomplete_tonal_function(
                component, key_signature)
            result.append(tonal_function)
        return result

    def analyze_neighbor_notes(self):
        r'''Is true when `note` in selection is preceeded by a stepwise interval
        in one direction and followed by a stepwise interval in
        the other direction. Otherwise false.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> selection = tonalanalysistools.select(staff[:])
                >>> selection.analyze_neighbor_notes()
                [False, False, False, False]

        Returns list of boolean values.
        '''
        result = []
        for component in self._client:
            tonal_function = self._is_neighbor_note(component)
            result.append(tonal_function)
        return result

    def analyze_passing_tones(self):
        r'''Is true when note in selection is both preceeded and followed
        by scalewise notes. Otherwise false.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> selection = tonalanalysistools.select(staff[:])
                >>> selection.analyze_passing_tones()
                [False, True, True, False]

        Returns list of boolean values.
        '''
        result = []
        for component in self._client:
            tonal_function = self._is_passing_tone(component)
            result.append(tonal_function)
        return result

    def analyze_tonal_functions(self, key_signature):
        r'''Analyzes tonal function of chords in selection
        according to `key_signature`.

        ..  container:: example

                >>> chord = Chord('<ef g bf>4')
                >>> key_signature = KeySignature('c', 'major')
                >>> selection = tonalanalysistools.select(chord)
                >>> selection.analyze_tonal_functions(key_signature)
                [FlatIIIMajorTriadInRootPosition]

        Returns none when no tonal function is understood.

        Returns list with elements each equal to tonal function or none.
        '''
        result = []
        for component in self._client:
            tonal_function = self._analyze_tonal_function(
                component, key_signature)
            result.append(tonal_function)
        return result

    def are_scalar_notes(self):
        r'''Is true when notes in selection are scalar.

        ::

            >>> selection_1.are_scalar_notes()
            True

        Otherwise false:

        ::


            >>> selection_2.are_scalar_notes()
            False

        Returns true or false.
        '''
        from abjad.tools import scoretools
        direction_string = None
        for left, right in sequencetools.iterate_sequence_nwise(
            iterate(self._client).by_class(scoretools.Note)):
            try:
                assert not (left.written_pitch == right.written_pitch)
                mdi = pitchtools.NamedInterval.from_pitch_carriers(
                    left, right)
                assert mdi.number <= 2
                if direction_string is None:
                    direction_string = mdi.direction_string
                assert direction_string == mdi.direction_string
            except AssertionError:
                return False
        return True

    def are_stepwise_ascending_notes(self):
        r'''Is true when notes in selection are stepwise ascending.

        ::

            >>> selection_1.are_stepwise_ascending_notes()
            True

        Otherwise false:

        ::

            >>> selection_2.are_stepwise_ascending_notes()
            False

        Returns true or false.
        '''
        from abjad.tools import scoretools
        for left, right in sequencetools.iterate_sequence_nwise(
            iterate(self._client).by_class(scoretools.Note)):
            try:
                assert not (left.written_pitch == right.written_pitch)
                mdi = pitchtools.NamedInterval.from_pitch_carriers(
                    left, right)
                assert mdi.number == 2
            except AssertionError:
                return False
        return True

    def are_stepwise_descending_notes(self):
        r'''Is true when notes in selection are stepwise descending.

        ::

            >>> selection_3 = tonalanalysistools.select(reversed(staff[:]))

        ::

            >>> selection_3.are_stepwise_descending_notes()
            True

        Otherwise false:

        ::

            >>> selection_1.are_stepwise_descending_notes()
            False

        ::

            >>> selection_2.are_stepwise_descending_notes()
            False

        Returns true or false.
        '''
        from abjad.tools import scoretools
        for left, right in sequencetools.iterate_sequence_nwise(
            iterate(self._client).by_class(scoretools.Note)):
            try:
                assert not (left.written_pitch == right.written_pitch)
                mdi = pitchtools.NamedInterval.from_pitch_carriers(
                    left, right)
                assert mdi.number == -2
            except AssertionError:
                return False
        return True

    def are_stepwise_notes(self):
        r'''Is true when notes in selection are stepwise.

        ::


            >>> selection_1.are_stepwise_notes()
            True

        Otherwise false:

        ::

            >>> selection_2.are_stepwise_notes()
            False

        Returns true or false.
        '''
        from abjad.tools import scoretools
        for left, right in sequencetools.iterate_sequence_nwise(
            iterate(self._client).by_class(scoretools.Note)):
            try:
                assert not (left.written_pitch == right.written_pitch)
                hdi = pitchtools.NamedInterval.from_pitch_carriers(
                    left, right)
                assert hdi.number <= 2
            except AssertionError:
                return False
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Returns client of mutation agent.

        Returns selection or component.
        '''
        return self._client
