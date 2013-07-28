from abjad.tools import iterationtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools.selectiontools.Selection import Selection


class TonalAnalysisSelection(Selection):
    r'''Tonal analysis selection.

    ::

        >>> staff = Staff("c'4 d' e' f'")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> selection_1 = tonalanalysistools.select(staff[:])

    ::

        >>> z(selection_1)
        tonalanalysistools.TonalAnalysisSelection(
            music=(Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4"))
            )

    Example 2. Disjunct selection:

    ::

        >>> notes = (staff[0], staff[3])
        >>> selection_2 = tonalanalysistools.select(notes)

    ::

        >>> z(selection_2)
        tonalanalysistools.TonalAnalysisSelection(
            music=(Note("c'4"), Note("f'4"))
            )

    '''

    ### PRIVATE METHODS ###

    @staticmethod
    def _analyze_chord(expr):
        from abjad.tools import tonalanalysistools
        from abjad.tools.tonalanalysistools import ChordQualityIndicator as CQI
        pitches = pitchtools.list_named_chromatic_pitches_in_expr(expr)
        npcset = pitchtools.NamedChromaticPitchClassSet(pitches)
        ordered_npcs = []
        letters = ('c', 'e', 'g', 'b', 'd', 'f', 'a')
        for letter in letters:
            for npc in npcset:
                if npc._diatonic_pitch_class_name == letter:
                    ordered_npcs.append(npc)
        ordered_npcs = pitchtools.NamedChromaticPitchClassSegment(ordered_npcs)
        for x in range(len(ordered_npcs)):
            ordered_npcs = ordered_npcs.rotate(1)
            segment = \
                ordered_npcs.inversion_equivalent_diatonic_interval_class_segment
            if segment.is_tertian:
                break
        else:
            return None
        root = ordered_npcs[0]
        indicator = CQI.from_diatonic_interval_class_segment(segment)
        bass = min(pitches).named_chromatic_pitch_class
        inversion = ordered_npcs.index(bass)
        return tonalanalysistools.ChordClass(
            root,
            indicator.quality_string,
            indicator.extent,
            inversion,
            )

    @staticmethod
    def _analyze_incomplete_chord(expr):
        from abjad.tools import tonalanalysistools
        pitches = pitchtools.list_named_chromatic_pitches_in_expr(expr)
        npcset = pitchtools.NamedChromaticPitchClassSet(pitches)
        dicv = npcset.inversion_equivalent_diatonic_interval_class_vector
        # TODO: eliminate code duplication #
        if dicv == TonalAnalysisSelection._make_dicv('c', 'ef'):
            model_npcs = ['c', 'ef']
            quality, extent = 'minor', 'triad'
        elif dicv == TonalAnalysisSelection._make_dicv('c', 'e'):
            model_npcs = ['c', 'e']
            quality, extent = 'major', 'triad'
        elif dicv == TonalAnalysisSelection._make_dicv('c', 'ef', 'bff'):
            model_npcs = ['c', 'ef', 'bff']
            quality, extent = 'diminished', 'seventh'
        elif dicv == TonalAnalysisSelection._make_dicv('c', 'ef', 'bf'):
            model_npcs = ['c', 'ef', 'bf']
            quality, extent = 'minor', 'seventh'
        elif dicv == TonalAnalysisSelection._make_dicv('c', 'e', 'bf'):
            model_npcs = ['c', 'e', 'bf']
            quality, extent = 'dominant', 'seventh'
        elif dicv == TonalAnalysisSelection._make_dicv('c', 'e', 'b'):
            model_npcs = ['c', 'e', 'b']
            quality, extent = 'major', 'seventh'
        else:
            message = 'can not identify incomplete tertian chord.'
            raise TonalHarmonyError(message)
        bass = min(pitches).named_chromatic_pitch_class
        try:
            npcseg = npcset.order_by(
                pitchtools.NamedChromaticPitchClassSegment(model_npcs))
        except ValueError:
            message = 'can not identify incomplete tertian chord.'
            raise TonalHarmonyError(message)
        inversion = npcseg.index(bass)
        root = npcseg[0]
        return tonalanalysistools.ChordClass(
            root,
            quality,
            extent,
            inversion,
            )

    @staticmethod
    def _analyze_tonal_function(expr, key_signature):
        from abjad.tools import tonalanalysistools
        if isinstance(expr, tonalanalysistools.ChordClass):
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
        scale_degree = scale.named_chromatic_pitch_class_to_scale_degree(root)
        quality = chord_class.quality_indicator.quality_string
        extent = chord_class.extent
        inversion = chord_class.inversion
        return tonalanalysistools.TonalFunction(
            scale_degree,
            quality,
            extent,
            inversion,
            )

    @staticmethod
    def _make_dicv(*named_chromatic_pitch_classes):
        npcset = pitchtools.NamedChromaticPitchClassSet(
            named_chromatic_pitch_classes)
        return npcset.inversion_equivalent_diatonic_interval_class_vector

    ### PUBLIC METHODS ###

    def analyze_chords(self):
        '''Analyze chords in selection:

        ::

            >>> chord = Chord([7, 10, 12, 16], (1, 4))
            >>> selection = tonalanalysistools.select(chord)
            >>> selection.analyze_chords()
            [CDominantSeventhInSecondInversion]

        Return none when no tonal chord is understood:

        ::

            >>> chord = Chord(['c', 'cs', 'd'], (1, 4))
            >>> selection = tonalanalysistools.select(chord)
            >>> selection.analyze_chords()
            [None]

        Raise tonal harmony error when chord in selection can not analyze.

        Return list with elements each equal to chord class or none.
        '''
        result = []
        for component in self:
            chord_class = self._analyze_chord(component)
            result.append(chord_class)
        return result

    def analyze_incomplete_chords(self):
        '''Analyze incomplete chords in selection:

        ::

            >>> chord = Chord("<g' b'>4")
            >>> selection = tonalanalysistools.select(chord)
            >>> selection.analyze_incomplete_chords()
            [GMajorTriadInRootPosition]

        ::

            >>> chord = Chord("<fs g b>4")
            >>> selection = tonalanalysistools.select(chord)
            >>> selection.analyze_incomplete_chords()
            [GMajorSeventhInSecondInversion]

        Raise tonal harmony error when chord in selection can not analyze.

        Return list with elements each equal to chord class or none.
        '''
        result = []
        for component in self:
            chord_class = self._analyze_incomplete_chord(component)
            result.append(chord_class)
        return result

    def analyze_tonal_functions(self, key_signature):
        '''Analyze tonal function of chords in selection 
        according to `key_signature`:

        ::

            >>> chord = Chord('<ef g bf>4')
            >>> key_signature = contexttools.KeySignatureMark('c', 'major')
            >>> selection = tonalanalysistools.select(chord)
            >>> selection.analyze_tonal_functions(key_signature)
            [FlatIIIMajorTriadInRootPosition]

        Return none when no tonal function is understood:

        ::

            >>> chord = Chord('<c cs d>4')
            >>> key_signature = contexttools.KeySignatureMark('c', 'major')
            >>> selection = tonalanalysistools.select(chord)
            >>> selection.analyze_tonal_functions(key_signature)
            [None]

        Raise tonal harmony error when chord in selection can not analyze.

        Return list with elements each equal to tonal function or none.
        '''
        result = []
        for component in self:
            tonal_function = self._analyze_tonal_function(
                component, key_signature)
            result.append(tonal_function)
        return result

    def are_scalar_notes(self):
        '''True when notes in selection are scalar:

        ::

            >>> selection_1.are_scalar_notes()
            True

        Otherwise false:

        ::


            >>> selection_2.are_scalar_notes()
            False

        Return boolean.
        '''
        direction_string = None
        for left, right in sequencetools.iterate_sequence_pairwise_strict(
            iterationtools.iterate_notes_in_expr(self)):
            try:
                assert not (left.written_pitch == right.written_pitch)
                mdi = pitchtools.calculate_melodic_diatonic_interval(
                    left, right)
                assert mdi.number <= 2
                if direction_string is None:
                    direction_string = mdi.direction_string
                assert direction_string == mdi.direction_string
            except AssertionError:
                return False
        return True

    def are_stepwise_ascending_notes(self):
        '''True when notes in `expr` are stepwise ascending:

        ::

            >>> selection_1.are_stepwise_ascending_notes()
            True

        Otherwise false:

        ::

            >>> selection_2.are_stepwise_ascending_notes()
            False

        Return boolean.
        '''
        for left, right in sequencetools.iterate_sequence_pairwise_strict(
            iterationtools.iterate_notes_in_expr(self)):
            try:
                assert not (left.written_pitch == right.written_pitch)
                mdi = pitchtools.calculate_melodic_diatonic_interval(
                    left, right)
                assert mdi.number == 2
            except AssertionError:
                return False
        return True

    def are_stepwise_descending_notes(self):
        '''True when notes in `expr` are stepwise descending.

        ::

            >>> selection_3 = tonalanalysistools.select(
            ...     reversed(selection_1))

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

        Return boolean.
        '''
        for left, right in sequencetools.iterate_sequence_pairwise_strict(
            iterationtools.iterate_notes_in_expr(self)):
            try:
                assert not (left.written_pitch == right.written_pitch)
                mdi = pitchtools.calculate_melodic_diatonic_interval(
                    left, right)
                assert mdi.number == -2
            except AssertionError:
                return False
        return True

    def are_stepwise_notes(self):
        '''True when notes in selection are stepwise:

        ::


            >>> selection_1.are_stepwise_notes()
            True

        Otherwise false:

        ::

            >>> selection_2.are_stepwise_notes()
            False

        Return boolean.
        '''
        for left, right in sequencetools.iterate_sequence_pairwise_strict(
            iterationtools.iterate_notes_in_expr(self)):
            try:
                assert not (left.written_pitch == right.written_pitch)
                hdi = pitchtools.calculate_harmonic_diatonic_interval(
                    left, right)
                assert hdi.number <= 2
            except AssertionError:
                return False
        return True
