# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import mathtools
from abjad.tools import pitchtools


class TonalAnalysisAgent(abctools.AbjadObject):
    r'''Tonal analysis agent.

    ::

        >>> import abjad
        >>> from abjad.tools import tonalanalysistools

    ..  container:: example

        Intializes agent on conjunct selection:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

        ::

            >>> agent_1 = abjad.analyze(staff[:])

    ..  container:: example

        Initializes agent on disjunct selection:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

        ::

            >>> agent_2 = abjad.analyze(staff[:1] + staff[-1:])

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
    def _analyze_chord(argument):
        from abjad.tools import tonalanalysistools
        pitches = pitchtools.PitchSegment.from_selection(argument)
        npcset = pitchtools.PitchClassSet(
            pitches,
            item_class=pitchtools.NamedPitchClass,
            )
        ordered_npcs = []
        letters = ('c', 'e', 'g', 'b', 'd', 'f', 'a')
        for letter in letters:
            for npc in npcset:
                if npc._get_diatonic_pitch_class_name() == letter:
                    ordered_npcs.append(npc)
        ordered_npcs = pitchtools.PitchClassSegment(
            ordered_npcs, item_class=pitchtools.NamedPitchClass)
        for x in range(len(ordered_npcs)):
            ordered_npcs = ordered_npcs.rotate(1)
            segment = pitchtools.IntervalClassSegment(
                    items=mathtools.difference_series(list(ordered_npcs)),
                    item_class=pitchtools.NamedInversionEquivalentIntervalClass,
                    )
            if segment.is_tertian:
                break
        else:
            return None
        root = ordered_npcs[0]
        class_ = tonalanalysistools.RootlessChordClass
        rootless_chord_class = class_.from_interval_class_segment(segment)
        bass = min(pitches).pitch_class
        inversion = ordered_npcs.index(bass)
        return tonalanalysistools.RootedChordClass(
            root,
            rootless_chord_class.quality_string,
            rootless_chord_class.extent,
            inversion,
            )

    @staticmethod
    def _analyze_incomplete_chord(argument):
        from abjad.tools import tonalanalysistools
        pitches = pitchtools.PitchSegment.from_selection(argument)
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
        bass = min(pitches).pitch_class
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
    def _analyze_incomplete_tonal_function(argument, key_signature):
        import abjad
        from abjad.tools import tonalanalysistools
        if isinstance(argument, tonalanalysistools.RootedChordClass):
            chord_class = argument
        else:
            agent = abjad.analyze(argument)
            chord_classes = agent.analyze_incomplete_chords()
            assert len(chord_classes) == 1
            chord_class = chord_classes[0]
        root = chord_class.root
        scale = tonalanalysistools.Scale(key_signature)
        scale_degree = scale.named_pitch_class_to_scale_degree(root)
        quality = chord_class.chord_quality.quality_string
        extent = chord_class.extent
        inversion = chord_class.inversion
        class_ = tonalanalysistools.RomanNumeral
        return class_.from_scale_degree_quality_extent_and_inversion(
            scale_degree,
            quality,
            extent,
            inversion,
            )

    @staticmethod
    def _analyze_tonal_function(argument, key_signature):
        import abjad
        from abjad.tools import tonalanalysistools
        if isinstance(argument, tonalanalysistools.RootedChordClass):
            chord_class = argument
        else:
            selection = abjad.analyze(argument)
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
        class_ = tonalanalysistools.RomanNumeral
        return class_.from_scale_degree_quality_extent_and_inversion(
            scale_degree,
            quality,
            extent,
            inversion,
            )

    @staticmethod
    def _is_neighbor_note(note):
        import abjad
        from abjad.tools import tonalanalysistools
        if not isinstance(note, abjad.Note):
            message = 'must be note: {!r}.'
            message = message.format(note)
            raise TypeError(message)
        previous_note = note._get_in_my_logical_voice(
            -1, prototype=abjad.Note)
        next_note = note._get_in_my_logical_voice(
            1, prototype=abjad.Note)
        if previous_note is None:
            return False
        if next_note is None:
            return False
        notes = [previous_note, note, next_note]
        selection = abjad.analyze(notes)
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
        import abjad
        from abjad.tools import tonalanalysistools
        if not isinstance(note, abjad.Note):
            message = 'must be note: {!r}.'
            message = message.format(note)
            raise TypeError(message)
        previous_note = note._get_in_my_logical_voice(
            -1, prototype=abjad.Note)
        next_note = note._get_in_my_logical_voice(
            1, prototype=abjad.Note)
        if previous_note is None or next_note is None:
            return False
        notes = [previous_note, note, next_note]
        selection = abjad.analyze(notes)
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
        r"""Analyzes chords in selection.

        ..  container:: example

            ::

                >>> chords = [
                ...     abjad.Chord([0, 4, 7], (1, 4)),
                ...     abjad.Chord([4, 7, 12], (1, 4)),
                ...     abjad.Chord([7, 12, 16], (1, 4)),
                ...     ]
                >>> staff = abjad.Staff(chords)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    <c' e' g'>4
                    <e' g' c''>4
                    <g' c'' e''>4
                }

            ::

                >>> for chord in abjad.analyze(staff[:]).analyze_chords():
                ...     chord
                ...
                CMajorTriadInRootPosition
                CMajorTriadInFirstInversion
                CMajorTriadInSecondInversion

        ..  container:: example

            The three inversions of an a minor triad:

            ::

                >>> chords = [
                ...     abjad.Chord([9, 12, 16], (1, 4)),
                ...     abjad.Chord([12, 16, 21], (1, 4)),
                ...     abjad.Chord([16, 21, 24], (1, 4)),
                ...     ]
                >>> staff = abjad.Staff(chords)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    <a' c'' e''>4
                    <c'' e'' a''>4
                    <e'' a'' c'''>4
                }

            ::

                >>> for chord in abjad.analyze(staff[:]).analyze_chords():
                ...     chord
                ...
                AMinorTriadInRootPosition
                AMinorTriadInFirstInversion
                AMinorTriadInSecondInversion

        ..  container:: example

            The four inversions of a C dominant seventh chord:

            ::

                >>> chords = [
                ...     abjad.Chord([0, 4, 7, 10], (1, 4)),
                ...     abjad.Chord([4, 7, 10, 12], (1, 4)),
                ...     abjad.Chord([7, 10, 12, 16], (1, 4)),
                ...     abjad.Chord([10, 12, 16, 19], (1, 4)),
                ...     ]
                >>> staff = abjad.Staff(chords)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    <c' e' g' bf'>4
                    <e' g' bf' c''>4
                    <g' bf' c'' e''>4
                    <bf' c'' e'' g''>4
                }

            ::

                >>> for chord in abjad.analyze(staff[:]).analyze_chords():
                ...     chord
                ...
                CDominantSeventhInRootPosition
                CDominantSeventhInFirstInversion
                CDominantSeventhInSecondInversion
                CDominantSeventhInThirdInversion

        ..  container:: example

            The five inversions of a C dominant ninth chord:

            ::

                >>> chords = [
                ...     abjad.Chord([0, 4, 7, 10, 14], (1, 4)),
                ...     abjad.Chord([4, 7, 10, 12, 14], (1, 4)),
                ...     abjad.Chord([7, 10, 12, 14, 16], (1, 4)),
                ...     abjad.Chord([10, 12, 14, 16, 19], (1, 4)),
                ...     abjad.Chord([2, 10, 12, 16, 19], (1, 4)),
                ...     ]
                >>> staff = abjad.Staff(chords)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    <c' e' g' bf' d''>4
                    <e' g' bf' c'' d''>4
                    <g' bf' c'' d'' e''>4
                    <bf' c'' d'' e'' g''>4
                    <d' bf' c'' e'' g''>4
                }

            ::

                >>> for chord in abjad.analyze(staff[:]).analyze_chords():
                ...     chord
                ...
                CDominantNinthInRootPosition
                CDominantNinthInFirstInversion
                CDominantNinthInSecondInversion
                CDominantNinthInThirdInversion
                CDominantNinthInFourthInversion

        Returns none when no tonal chord is understood.

        Returns list with elements each equal to chord class or none.
        """
        result = []
        for component in self._client:
            chord_class = self._analyze_chord(component)
            result.append(chord_class)
        return result

    def analyze_incomplete_chords(self):
        r'''Analyzes incomplete chords.

        ..  container:: example

            ::

                >>> chord = abjad.Chord("<g' b'>4")
                >>> abjad.analyze(chord).analyze_incomplete_chords()
                [GMajorTriadInRootPosition]

            ::

                >>> chord = abjad.Chord("<g' bf'>4")
                >>> abjad.analyze(chord).analyze_incomplete_chords()
                [GMinorTriadInRootPosition]

            ::

                >>> chord = abjad.Chord("<f g b>4")
                >>> abjad.analyze(chord).analyze_incomplete_chords()
                [GDominantSeventhInSecondInversion]

            ::

                >>> chord = abjad.Chord("<fs g b>4")
                >>> abjad.analyze(chord).analyze_incomplete_chords()
                [GMajorSeventhInSecondInversion]

        Raises tonal harmony error when chord in client can not analyze.

        Returns list with elements each equal to chord class or none.
        '''
        result = []
        for component in self._client:
            chord_class = self._analyze_incomplete_chord(component)
            result.append(chord_class)
        return result

    def analyze_incomplete_tonal_functions(self, key_signature):
        r'''Analyzes incomplete tonal functions of chords in client
        according to `key_signature`.

        ..  container:: example

            ::

                >>> chord = abjad.Chord("<c' e'>4")
                >>> key_signature = abjad.KeySignature('g', 'major')
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_incomplete_tonal_functions(key_signature)
                [RomanNumeral('IV')]

            ::

                >>> chord = abjad.Chord("<g' b'>4")
                >>> key_signature = abjad.KeySignature('c', 'major')
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_incomplete_tonal_functions(key_signature)
                [RomanNumeral('V')]

            ::

                >>> chord = abjad.Chord("<g' bf'>4")
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_incomplete_tonal_functions(key_signature)
                [RomanNumeral('v')]

            ::

                >>> key_signature = abjad.KeySignature('c', 'major')
                >>> chord = abjad.Chord("<f g b>4")
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_incomplete_tonal_functions(key_signature)
                [RomanNumeral('V4/3')]

            ::

                >>> chord = abjad.Chord("<fs g b>4")
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_incomplete_tonal_functions(key_signature)
                [RomanNumeral('VM4/3')]

        Raises tonal harmony error when chord in client can not analyze.

        Returns list with elements each equal to tonal function or none.
        '''
        result = []
        for component in self._client:
            tonal_function = self._analyze_incomplete_tonal_function(
                component,
                key_signature,
                )
            result.append(tonal_function)
        return result

    def analyze_neighbor_notes(self):
        r'''Is true when `note` in client is preceeded by a stepwise interval
        in one direction and followed by a stepwise interval in the other
        direction. Otherwise false.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8
                    d'8
                    e'8
                    f'8
                }

            ::

                >>> agent = abjad.analyze(staff[:])
                >>> agent.analyze_neighbor_notes()
                [False, False, False, False]

        Returns list of boolean values.
        '''
        result = []
        for component in self._client:
            tonal_function = self._is_neighbor_note(component)
            result.append(tonal_function)
        return result

    def analyze_passing_tones(self):
        r'''Is true when note in client is both preceeded and followed by
        scalewise notes. Otherwise false.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> show(staff) # doctest: +SKIP

            ..  docs::
                
                >>> f(staff)
                \new Staff {
                    c'8
                    d'8
                    e'8
                    f'8
                }

            ::

                >>> agent = abjad.analyze(staff[:])
                >>> agent.analyze_passing_tones()
                [False, True, True, False]

        Returns list of boolean values.
        '''
        result = []
        for component in self._client:
            tonal_function = self._is_passing_tone(component)
            result.append(tonal_function)
        return result

    def analyze_tonal_functions(self, key_signature):
        r'''Analyzes tonal function of chords in client according to
        `key_signature`.

        ..  container:: example

                >>> chord = abjad.Chord('<ef g bf>4')
                >>> key_signature = abjad.KeySignature('c', 'major')
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('bIII')]

            ::

                >>> key_signature = abjad.KeySignature('c', 'major')
                >>> chord = abjad.Chord('<c e g>4')
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('I')]

            ::

                >>> chord = abjad.Chord(['e', 'g', "c'"], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('I6')]

            ::

                >>> chord = abjad.Chord(['g', "c'", "e'"], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('I6/4')]

        ..  container:: example

            ::

                >>> key_signature = abjad.KeySignature('c', 'major')
                >>> chord = abjad.Chord(['c', 'ef', 'g'], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('i')]

            ::

                >>> chord = abjad.Chord(['ef', 'g', "c'"], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('i6')]

            ::

                >>> chord = abjad.Chord(['g', "c'", "ef'"], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('i6/4')]

        ..  container:: example

            ::

                >>> key_signature = abjad.KeySignature('c', 'major')
                >>> chord = abjad.Chord(['c', 'e', 'g', 'bf'], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('I7')]

            ::

                >>> chord = abjad.Chord(['e', 'g', 'bf', "c'"], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('I6/5')]

            ::

                >>> chord = abjad.Chord(['g', 'bf', "c'", "e'"], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('I4/3')]

            ::

                >>> chord = abjad.Chord(['bf', "c'", "e'", "g'"], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [RomanNumeral('I4/2')]

        ..  container:: example

            ::

                >>> key_signature = abjad.KeySignature('c', 'major')
                >>> chord = abjad.Chord(['c', 'cs', 'd'], (1, 4))
                >>> agent = abjad.analyze(chord)
                >>> agent.analyze_tonal_functions(key_signature)
                [None]

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
        r'''Is true when notes in client are scalar. Otherwise false

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 cs'")
                >>> abjad.analyze(staff[:]).are_scalar_notes()
                True

            ::

                >>> staff = abjad.Staff("c'4 d'")
                >>> abjad.analyze(staff[:]).are_scalar_notes()
                True

            ::

                >>> staff = abjad.Staff("c'4 ds'")
                >>> abjad.analyze(staff[:]).are_scalar_notes()
                True

            ::

                >>> staff = abjad.Staff("c'4 b")
                >>> abjad.analyze(staff[:]).are_scalar_notes()
                True

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 c'")
                >>> abjad.analyze(staff[:]).are_scalar_notes()
                False

            ::

                >>> staff = abjad.Staff("c'4 e'")
                >>> abjad.analyze(staff[:]).are_scalar_notes()
                False

        Returns true or false.
        '''
        import abjad
        direction_string = None
        notes = abjad.iterate(self._client).by_class(abjad.Note)
        for left, right in abjad.Sequence(notes).nwise():
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
        r'''Is true when notes in client are stepwise ascending. Otherwise
        false.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 cs'")
                >>> abjad.analyze(staff[:]).are_stepwise_ascending_notes()
                False

            ::

                >>> staff = abjad.Staff("c'4 d'")
                >>> abjad.analyze(staff[:]).are_stepwise_ascending_notes()
                True

            ::

                >>> staff = abjad.Staff("c'4 ds'")
                >>> abjad.analyze(staff[:]).are_stepwise_ascending_notes()
                True

            ::

                >>> staff = abjad.Staff("c'4 b")
                >>> abjad.analyze(staff[:]).are_stepwise_ascending_notes()
                False

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 c'")
                >>> abjad.analyze(staff[:]).are_stepwise_ascending_notes()
                False

            ::

                >>> staff = abjad.Staff("c'4 e'")
                >>> abjad.analyze(staff[:]).are_stepwise_ascending_notes()
                False

        Returns true or false.
        '''
        import abjad
        notes = abjad.iterate(self._client).by_class(abjad.Note)
        for left, right in abjad.Sequence(notes).nwise():
            try:
                assert not (left.written_pitch == right.written_pitch)
                mdi = pitchtools.NamedInterval.from_pitch_carriers(
                    left, right)
                assert mdi.number == 2
            except AssertionError:
                return False
        return True

    def are_stepwise_descending_notes(self):
        r'''Is true when notes in client are stepwise descending. Otherwise
        false.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 cs'")
                >>> abjad.analyze(staff[:]).are_stepwise_descending_notes()
                False

            ::

                >>> staff = abjad.Staff("c'4 d'")
                >>> abjad.analyze(staff[:]).are_stepwise_descending_notes()
                False

            ::

                >>> staff = abjad.Staff("c'4 ds'")
                >>> abjad.analyze(staff[:]).are_stepwise_descending_notes()
                False

            ::

                >>> staff = abjad.Staff("c'4 b")
                >>> abjad.analyze(staff[:]).are_stepwise_descending_notes()
                True

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 c'")
                >>> abjad.analyze(staff[:]).are_stepwise_descending_notes()
                False

            ::

                >>> staff = abjad.Staff("c'4 e'")
                >>> abjad.analyze(staff[:]).are_stepwise_descending_notes()
                False

        Returns true or false.
        '''
        import abjad
        notes = abjad.iterate(self._client).by_class(abjad.Note)
        for left, right in abjad.Sequence(notes).nwise():
            try:
                assert not (left.written_pitch == right.written_pitch)
                mdi = pitchtools.NamedInterval.from_pitch_carriers(
                    left, right)
                assert mdi.number == -2
            except AssertionError:
                return False
        return True

    def are_stepwise_notes(self):
        r'''Is true when notes in client are stepwise. Otherwise false.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 cs'")
                >>> abjad.analyze(staff[:]).are_stepwise_notes()
                True

            ::

                >>> staff = abjad.Staff("c'4 d'")
                >>> abjad.analyze(staff[:]).are_stepwise_notes()
                True

            ::

                >>> staff = abjad.Staff("c'4 ds'")
                >>> abjad.analyze(staff[:]).are_stepwise_notes()
                True

            ::

                >>> staff = abjad.Staff("c'4 b")
                >>> abjad.analyze(staff[:]).are_stepwise_notes()
                True

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 c'")
                >>> abjad.analyze(staff[:]).are_stepwise_notes()
                False

            ::

                >>> staff = abjad.Staff("c'4 e'")
                >>> abjad.analyze(staff[:]).are_stepwise_notes()
                False

        Returns true or false.
        '''
        import abjad
        notes = abjad.iterate(self._client).by_class(abjad.Note)
        for left, right in abjad.Sequence(notes).nwise():
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
        r'''Gets client.

        Returns selection or component.
        '''
        return self._client
