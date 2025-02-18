import typing

from . import lyenv as _lyenv


class LilyPondContext:
    r"""
    LilyPond context.

    ..  container:: example

        >>> context = abjad.LilyPondContext('MensuralStaff')
        >>> context
        LilyPondContext(name='MensuralStaff')

        >>> for lilypond_context in abjad.LilyPondContext.list_all_contexts():
        ...     is_global_context = 'X' if lilypond_context.is_global_context else ' '
        ...     is_score_context = 'X' if lilypond_context.is_score_context else ' '
        ...     is_staff_group_context = 'X' if lilypond_context.is_staff_group_context else ' '
        ...     is_staff_context = 'X' if lilypond_context.is_staff_context else ' '
        ...     is_bottom_context = 'X' if lilypond_context.is_bottom_context else ' '
        ...     print('[{}] [{}] [{}] [{}] [{}] {}'.format(
        ...         is_global_context,
        ...         is_score_context,
        ...         is_staff_group_context,
        ...         is_staff_context,
        ...         is_bottom_context,
        ...         lilypond_context.name,
        ...         ))
        ...
        [ ] [ ] [X] [ ] [ ] ChoirStaff
        [ ] [ ] [ ] [ ] [X] ChordNames
        [ ] [ ] [ ] [ ] [X] CueVoice
        [ ] [ ] [ ] [ ] [X] Devnull
        [ ] [ ] [ ] [X] [ ] DrumStaff
        [ ] [ ] [ ] [ ] [X] DrumVoice
        [ ] [ ] [ ] [ ] [X] Dynamics
        [ ] [ ] [ ] [ ] [X] FiguredBass
        [ ] [ ] [ ] [ ] [X] FretBoards
        [X] [ ] [ ] [ ] [ ] Global
        [ ] [ ] [X] [ ] [ ] GrandStaff
        [ ] [ ] [ ] [X] [ ] GregorianTranscriptionStaff
        [ ] [ ] [ ] [ ] [X] GregorianTranscriptionVoice
        [ ] [ ] [ ] [X] [ ] KievanStaff
        [ ] [ ] [ ] [ ] [X] KievanVoice
        [ ] [ ] [ ] [ ] [X] Lyrics
        [ ] [ ] [ ] [X] [ ] MensuralStaff
        [ ] [ ] [ ] [ ] [X] MensuralVoice
        [ ] [ ] [ ] [ ] [X] NoteNames
        [ ] [ ] [ ] [ ] [X] NullVoice
        [ ] [ ] [X] [ ] [ ] OneStaff
        [ ] [ ] [ ] [X] [ ] PetrucciStaff
        [ ] [ ] [ ] [ ] [X] PetrucciVoice
        [ ] [ ] [X] [ ] [ ] PianoStaff
        [ ] [ ] [ ] [X] [ ] RhythmicStaff
        [ ] [X] [ ] [ ] [ ] Score
        [ ] [ ] [ ] [X] [ ] Staff
        [ ] [ ] [X] [ ] [ ] StaffGroup
        [ ] [ ] [ ] [X] [ ] TabStaff
        [ ] [ ] [ ] [ ] [X] TabVoice
        [ ] [ ] [ ] [X] [ ] VaticanaStaff
        [ ] [ ] [ ] [ ] [X] VaticanaVoice
        [ ] [ ] [ ] [ ] [X] Voice

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_name",)

    _identity_map: dict[str, "LilyPondContext"] = {}

    ### CONSTRUCTOR ###

    def __new__(class_, name="Voice"):
        if isinstance(name, class_):
            name = name.name
        if name in class_._identity_map:
            obj = class_._identity_map[name]
        else:
            obj = object.__new__(class_)
            class_._identity_map[name] = obj
        return obj

    ### INITIALIZER ###

    def __init__(self, name="Voice") -> None:
        assert name in _lyenv.contexts
        self._name = name

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(name={self.name!r})"

    ### PUBLIC PROPERTIES ###

    @property
    def accepted_by(self) -> tuple["LilyPondContext", ...]:
        r"""
        Gets contexts accepting LilyPond context.

        ..  container:: example

            >>> context = abjad.LilyPondContext('MensuralStaff')
            >>> for accepting_context in context.accepted_by:
            ...     accepting_context
            ...
            LilyPondContext(name='OneStaff')
            LilyPondContext(name='Score')

            >>> for lilypond_context in abjad.LilyPondContext.list_all_contexts():
            ...     print(f'{lilypond_context.name}:')
            ...     accepted_by = lilypond_context.accepted_by
            ...     if accepted_by:
            ...         accepted_by = ',\n    '.join(_.name for _ in accepted_by)
            ...         print(f'    {accepted_by}')
            ...
            ChoirStaff:
                ChoirStaff,
                Score,
                StaffGroup
            ChordNames:
                ChoirStaff,
                GrandStaff,
                OneStaff,
                PianoStaff,
                Score,
                StaffGroup
            CueVoice:
                DrumStaff,
                GregorianTranscriptionStaff,
                KievanStaff,
                MensuralStaff,
                PetrucciStaff,
                RhythmicStaff,
                Staff,
                TabStaff,
                VaticanaStaff
            Devnull:
                Score
            DrumStaff:
                ChoirStaff,
                GrandStaff,
                OneStaff,
                PianoStaff,
                Score,
                StaffGroup
            DrumVoice:
                DrumStaff
            Dynamics:
                ChoirStaff,
                GrandStaff,
                OneStaff,
                PianoStaff,
                Score
            FiguredBass:
                ChoirStaff,
                GrandStaff,
                OneStaff,
                PianoStaff,
                Score,
                StaffGroup
            FretBoards:
                OneStaff,
                Score,
                StaffGroup
            Global:
            GrandStaff:
                ChoirStaff,
                Score,
                StaffGroup
            GregorianTranscriptionStaff:
                OneStaff,
                Score
            GregorianTranscriptionVoice:
                GregorianTranscriptionStaff
            KievanStaff:
                OneStaff,
                Score
            KievanVoice:
                KievanStaff
            Lyrics:
                ChoirStaff,
                GrandStaff,
                OneStaff,
                PianoStaff,
                Score,
                StaffGroup
            MensuralStaff:
                OneStaff,
                Score
            MensuralVoice:
                MensuralStaff
            NoteNames:
                OneStaff,
                Score
            NullVoice:
                DrumStaff,
                GregorianTranscriptionStaff,
                KievanStaff,
                MensuralStaff,
                PetrucciStaff,
                RhythmicStaff,
                Staff,
                TabStaff,
                VaticanaStaff
            OneStaff:
                ChoirStaff,
                Score,
                StaffGroup
            PetrucciStaff:
                OneStaff,
                Score
            PetrucciVoice:
                PetrucciStaff
            PianoStaff:
                ChoirStaff,
                Score,
                StaffGroup
            RhythmicStaff:
                ChoirStaff,
                GrandStaff,
                OneStaff,
                PianoStaff,
                Score,
                StaffGroup
            Score:
                Global
            Staff:
                ChoirStaff,
                GrandStaff,
                OneStaff,
                PianoStaff,
                Score,
                StaffGroup
            StaffGroup:
                ChoirStaff,
                Score,
                StaffGroup
            TabStaff:
                GrandStaff,
                OneStaff,
                PianoStaff,
                Score,
                StaffGroup
            TabVoice:
                TabStaff
            VaticanaStaff:
                OneStaff,
                Score
            VaticanaVoice:
                VaticanaStaff
            Voice:
                RhythmicStaff,
                Staff

        """
        accepting_contexts = set()
        for lilypond_type, context_info in _lyenv.contexts.items():
            assert isinstance(context_info, dict), repr(context_info)
            if self.name in context_info["accepts"]:
                accepting_context = LilyPondContext(lilypond_type)
                accepting_contexts.add(accepting_context)
        return tuple(sorted(accepting_contexts, key=lambda x: x.name))

    @property
    def accepts(self) -> tuple["LilyPondContext", ...]:
        r"""
        Gets contexts accepted by LilyPond context.

        ..  container:: example

            >>> context = abjad.LilyPondContext('MensuralStaff')
            >>> for accepted_context in context.accepts:
            ...     accepted_context
            ...
            LilyPondContext(name='CueVoice')
            LilyPondContext(name='MensuralVoice')
            LilyPondContext(name='NullVoice')

        """
        dictionary = _lyenv.contexts[self.name]
        assert isinstance(dictionary, dict), repr(dictionary)
        accepts = (LilyPondContext(name=name) for name in dictionary["accepts"])
        return tuple(sorted(accepts, key=lambda x: x.name))

    @property
    def alias(self) -> typing.Optional["LilyPondContext"]:
        r"""
        Gets alias of LilyPond context.

        ..  container:: example

            >>> context = abjad.LilyPondContext('MensuralStaff')
            >>> context.alias
            LilyPondContext(name='Staff')

        """
        dictionary = _lyenv.contexts[self.name]
        assert isinstance(dictionary, dict)
        aliases = dictionary["aliases"]
        if aliases:
            alias = tuple(aliases)[0]
            if alias not in _lyenv.contexts:
                return None
            return LilyPondContext(name=alias)
        return None

    @property
    def default_child(self) -> typing.Optional["LilyPondContext"]:
        r"""
        Gets default child of LilyPond context.

        ..  container:: example

            >>> context = abjad.LilyPondContext('MensuralStaff')
            >>> context.default_child
            LilyPondContext(name='MensuralVoice')

            >>> for lilypond_context in abjad.LilyPondContext.list_all_contexts():
            ...     print(f'{lilypond_context.name}:')
            ...     default_child = lilypond_context.default_child
            ...     if default_child:
            ...         print(f'    {default_child.name}')
            ...
            ChoirStaff:
                Staff
            ChordNames:
            CueVoice:
            Devnull:
            DrumStaff:
                DrumVoice
            DrumVoice:
            Dynamics:
            FiguredBass:
            FretBoards:
            Global:
                Score
            GrandStaff:
                Staff
            GregorianTranscriptionStaff:
                GregorianTranscriptionVoice
            GregorianTranscriptionVoice:
            KievanStaff:
                KievanVoice
            KievanVoice:
            Lyrics:
            MensuralStaff:
                MensuralVoice
            MensuralVoice:
            NoteNames:
            NullVoice:
            OneStaff:
                Staff
            PetrucciStaff:
                PetrucciVoice
            PetrucciVoice:
            PianoStaff:
                Staff
            RhythmicStaff:
                Voice
            Score:
                Staff
            Staff:
                Voice
            StaffGroup:
                Staff
            TabStaff:
                TabVoice
            TabVoice:
            VaticanaStaff:
                VaticanaVoice
            VaticanaVoice:
            Voice:

        """
        if self.is_bottom_context:
            return None
        dictionary = _lyenv.contexts[self.name]
        assert isinstance(dictionary, dict), repr(dictionary)
        default_child_name = dictionary.get("default_child", None)
        if default_child_name is None:
            alias = self.alias
            if alias is not None:
                return alias.default_child
        if default_child_name and default_child_name in _lyenv.contexts:
            return LilyPondContext(name=default_child_name)
        return None

    @property
    def engravers(self) -> tuple["LilyPondEngraver", ...]:
        r"""
        Gets engravers belonging to LilyPond context.

        ..  container:: example

            >>> context = abjad.LilyPondContext('MensuralStaff')
            >>> for engraver in context.engravers:
            ...     engraver
            ...
            LilyPondEngraver(name='Accidental_engraver')
            LilyPondEngraver(name='Axis_group_engraver')
            LilyPondEngraver(name='Bar_engraver')
            LilyPondEngraver(name='Clef_engraver')
            LilyPondEngraver(name='Collision_engraver')
            LilyPondEngraver(name='Cue_clef_engraver')
            LilyPondEngraver(name='Custos_engraver')
            LilyPondEngraver(name='Dot_column_engraver')
            LilyPondEngraver(name='Figured_bass_engraver')
            LilyPondEngraver(name='Figured_bass_position_engraver')
            LilyPondEngraver(name='Fingering_column_engraver')
            LilyPondEngraver(name='Font_size_engraver')
            LilyPondEngraver(name='Grob_pq_engraver')
            LilyPondEngraver(name='Instrument_name_engraver')
            LilyPondEngraver(name='Key_engraver')
            LilyPondEngraver(name='Ledger_line_engraver')
            LilyPondEngraver(name='Ottava_spanner_engraver')
            LilyPondEngraver(name='Output_property_engraver')
            LilyPondEngraver(name='Piano_pedal_align_engraver')
            LilyPondEngraver(name='Piano_pedal_engraver')
            LilyPondEngraver(name='Pure_from_neighbor_engraver')
            LilyPondEngraver(name='Rest_collision_engraver')
            LilyPondEngraver(name='Script_row_engraver')
            LilyPondEngraver(name='Separating_line_group_engraver')
            LilyPondEngraver(name='Staff_collecting_engraver')
            LilyPondEngraver(name='Staff_symbol_engraver')
            LilyPondEngraver(name='Time_signature_engraver')

        """
        engravers = set()
        dictionary = _lyenv.contexts[self.name]
        assert isinstance(dictionary, dict), repr(dictionary)
        for engraver_name in dictionary["consists"]:
            engraver = LilyPondEngraver(name=engraver_name)
            engravers.add(engraver)
        engravers_ = tuple(sorted(engravers, key=lambda x: x.name))
        return engravers_

    @property
    def grobs(self) -> tuple["LilyPondGrob", ...]:
        r"""
        Gets grobs created by LilyPond context.

        ..  container:: example

            >>> context = abjad.LilyPondContext('MensuralStaff')
            >>> for grob in context.grobs:
            ...     grob
            ...
            LilyPondGrob(name='Accidental')
            LilyPondGrob(name='AccidentalCautionary')
            LilyPondGrob(name='AccidentalPlacement')
            LilyPondGrob(name='AccidentalSuggestion')
            LilyPondGrob(name='BarLine')
            LilyPondGrob(name='BassFigure')
            LilyPondGrob(name='BassFigureAlignment')
            LilyPondGrob(name='BassFigureAlignmentPositioning')
            LilyPondGrob(name='BassFigureBracket')
            LilyPondGrob(name='BassFigureContinuation')
            LilyPondGrob(name='BassFigureLine')
            LilyPondGrob(name='Clef')
            LilyPondGrob(name='ClefModifier')
            LilyPondGrob(name='CueClef')
            LilyPondGrob(name='CueEndClef')
            LilyPondGrob(name='Custos')
            LilyPondGrob(name='DotColumn')
            LilyPondGrob(name='FingeringColumn')
            LilyPondGrob(name='InstrumentName')
            LilyPondGrob(name='KeyCancellation')
            LilyPondGrob(name='KeySignature')
            LilyPondGrob(name='LedgerLineSpanner')
            LilyPondGrob(name='NoteCollision')
            LilyPondGrob(name='OttavaBracket')
            LilyPondGrob(name='PianoPedalBracket')
            LilyPondGrob(name='RestCollision')
            LilyPondGrob(name='ScriptRow')
            LilyPondGrob(name='SostenutoPedal')
            LilyPondGrob(name='SostenutoPedalLineSpanner')
            LilyPondGrob(name='StaffSpacing')
            LilyPondGrob(name='StaffSymbol')
            LilyPondGrob(name='SustainPedal')
            LilyPondGrob(name='SustainPedalLineSpanner')
            LilyPondGrob(name='TimeSignature')
            LilyPondGrob(name='UnaCordaPedal')
            LilyPondGrob(name='UnaCordaPedalLineSpanner')
            LilyPondGrob(name='VerticalAxisGroup')

        """
        grobs: typing.Set[LilyPondGrob] = set()
        for engraver in self.engravers:
            grobs.update(engraver.grobs)
        return tuple(sorted(grobs, key=lambda x: x.name))

    @property
    def is_bottom_context(self) -> bool:
        r"""
        Is true if LilyPond context is a bottom context.

        ..  container:: example

            >>> for lilypond_context in abjad.LilyPondContext.list_all_contexts():
            ...     is_bottom_context = 'X' if lilypond_context.is_bottom_context else ' '
            ...     print(f'[{is_bottom_context}] {lilypond_context.name}')
            ...
            [ ] ChoirStaff
            [X] ChordNames
            [X] CueVoice
            [X] Devnull
            [ ] DrumStaff
            [X] DrumVoice
            [X] Dynamics
            [X] FiguredBass
            [X] FretBoards
            [ ] Global
            [ ] GrandStaff
            [ ] GregorianTranscriptionStaff
            [X] GregorianTranscriptionVoice
            [ ] KievanStaff
            [X] KievanVoice
            [X] Lyrics
            [ ] MensuralStaff
            [X] MensuralVoice
            [X] NoteNames
            [X] NullVoice
            [ ] OneStaff
            [ ] PetrucciStaff
            [X] PetrucciVoice
            [ ] PianoStaff
            [ ] RhythmicStaff
            [ ] Score
            [ ] Staff
            [ ] StaffGroup
            [ ] TabStaff
            [X] TabVoice
            [ ] VaticanaStaff
            [X] VaticanaVoice
            [X] Voice

        """
        if not self.accepts:
            return True
        return False

    @property
    def is_custom(self) -> bool:
        r"""
        Is true if LilyPond context is user-created.

        ..  container:: example

            >>> context = abjad.LilyPondContext('MensuralStaff')
            >>> context.is_custom
            False

        """
        dictionary = _lyenv.contexts[self.name]
        assert isinstance(dictionary, dict), repr(dictionary)
        return bool(dictionary.get("is_custom", False))

    @property
    def is_global_context(self) -> bool:
        r"""
        Is true if LilyPond context is a global context.

        ..  container:: example

            >>> for lilypond_context in abjad.LilyPondContext.list_all_contexts():
            ...     is_global_context = 'X' if lilypond_context.is_global_context else ' '
            ...     print(f'[{is_global_context}] {lilypond_context.name}')
            ...
            [ ] ChoirStaff
            [ ] ChordNames
            [ ] CueVoice
            [ ] Devnull
            [ ] DrumStaff
            [ ] DrumVoice
            [ ] Dynamics
            [ ] FiguredBass
            [ ] FretBoards
            [X] Global
            [ ] GrandStaff
            [ ] GregorianTranscriptionStaff
            [ ] GregorianTranscriptionVoice
            [ ] KievanStaff
            [ ] KievanVoice
            [ ] Lyrics
            [ ] MensuralStaff
            [ ] MensuralVoice
            [ ] NoteNames
            [ ] NullVoice
            [ ] OneStaff
            [ ] PetrucciStaff
            [ ] PetrucciVoice
            [ ] PianoStaff
            [ ] RhythmicStaff
            [ ] Score
            [ ] Staff
            [ ] StaffGroup
            [ ] TabStaff
            [ ] TabVoice
            [ ] VaticanaStaff
            [ ] VaticanaVoice
            [ ] Voice

        """
        if not self.accepts:
            return False
        elif self is type(self)("Global"):
            return True
        elif self.alias is type(self)("Global"):
            return True
        return False

    @property
    def is_score_context(self) -> bool:
        r"""
        Is true if LilyPond context is a score context.

        ..  container:: example

            >>> for lilypond_context in abjad.LilyPondContext.list_all_contexts():
            ...     is_score_context = 'X' if lilypond_context.is_score_context else ' '
            ...     print(f'[{is_score_context}] {lilypond_context.name}')
            ...
            [ ] ChoirStaff
            [ ] ChordNames
            [ ] CueVoice
            [ ] Devnull
            [ ] DrumStaff
            [ ] DrumVoice
            [ ] Dynamics
            [ ] FiguredBass
            [ ] FretBoards
            [ ] Global
            [ ] GrandStaff
            [ ] GregorianTranscriptionStaff
            [ ] GregorianTranscriptionVoice
            [ ] KievanStaff
            [ ] KievanVoice
            [ ] Lyrics
            [ ] MensuralStaff
            [ ] MensuralVoice
            [ ] NoteNames
            [ ] NullVoice
            [ ] OneStaff
            [ ] PetrucciStaff
            [ ] PetrucciVoice
            [ ] PianoStaff
            [ ] RhythmicStaff
            [X] Score
            [ ] Staff
            [ ] StaffGroup
            [ ] TabStaff
            [ ] TabVoice
            [ ] VaticanaStaff
            [ ] VaticanaVoice
            [ ] Voice

        """
        if not self.accepts:
            return False
        elif self is type(self)("Score"):
            return True
        elif self.alias is type(self)("Score"):
            return True
        return False

    @property
    def is_staff_context(self) -> bool:
        r"""
        Is true if LilyPond context is a staff context.

        ..  container:: example

            >>> for lilypond_context in abjad.LilyPondContext.list_all_contexts():
            ...     is_staff_context = 'X' if lilypond_context.is_staff_context else ' '
            ...     print(f'[{is_staff_context}] {lilypond_context.name}')
            ...
            [ ] ChoirStaff
            [ ] ChordNames
            [ ] CueVoice
            [ ] Devnull
            [X] DrumStaff
            [ ] DrumVoice
            [ ] Dynamics
            [ ] FiguredBass
            [ ] FretBoards
            [ ] Global
            [ ] GrandStaff
            [X] GregorianTranscriptionStaff
            [ ] GregorianTranscriptionVoice
            [X] KievanStaff
            [ ] KievanVoice
            [ ] Lyrics
            [X] MensuralStaff
            [ ] MensuralVoice
            [ ] NoteNames
            [ ] NullVoice
            [ ] OneStaff
            [X] PetrucciStaff
            [ ] PetrucciVoice
            [ ] PianoStaff
            [X] RhythmicStaff
            [ ] Score
            [X] Staff
            [ ] StaffGroup
            [X] TabStaff
            [ ] TabVoice
            [X] VaticanaStaff
            [ ] VaticanaVoice
            [ ] Voice

        """
        if not self.accepts:
            return False
        elif self is type(self)("Staff"):
            return True
        elif self.alias is type(self)("Staff"):
            return True
        return False

    @property
    def is_staff_group_context(self) -> bool:
        r"""
        Is true if LilyPond context is a staff group context.

        ..  container:: example

            >>> for lilypond_context in abjad.LilyPondContext.list_all_contexts():
            ...     is_staff_group_context = 'X' if lilypond_context.is_staff_group_context else ' '
            ...     print(f'[{is_staff_group_context}] {lilypond_context.name}')
            ...
            [X] ChoirStaff
            [ ] ChordNames
            [ ] CueVoice
            [ ] Devnull
            [ ] DrumStaff
            [ ] DrumVoice
            [ ] Dynamics
            [ ] FiguredBass
            [ ] FretBoards
            [ ] Global
            [X] GrandStaff
            [ ] GregorianTranscriptionStaff
            [ ] GregorianTranscriptionVoice
            [ ] KievanStaff
            [ ] KievanVoice
            [ ] Lyrics
            [ ] MensuralStaff
            [ ] MensuralVoice
            [ ] NoteNames
            [ ] NullVoice
            [X] OneStaff
            [ ] PetrucciStaff
            [ ] PetrucciVoice
            [X] PianoStaff
            [ ] RhythmicStaff
            [ ] Score
            [ ] Staff
            [X] StaffGroup
            [ ] TabStaff
            [ ] TabVoice
            [ ] VaticanaStaff
            [ ] VaticanaVoice
            [ ] Voice

        """
        return not any(
            [
                self.is_global_context,
                self.is_score_context,
                self.is_staff_context,
                self.is_bottom_context,
            ]
        )

    @property
    def name(self) -> str:
        r"""
        Gets name of LilyPond context.

        ..  container:: example

            >>> context = abjad.LilyPondContext('MensuralStaff')
            >>> context.name
            'MensuralStaff'

        """
        return self._name

    @property
    def property_names(self) -> tuple[str, ...]:
        r"""
        Gets property names of LilyPond context.

        ..  container:: example

            >>> context = abjad.LilyPondContext('MensuralStaff')
            >>> for property_name in context.property_names:
            ...     property_name
            ...
            'accidentalGrouping'
            'autoAccidentals'
            'autoCautionaries'
            'busyGrobs'
            'clefGlyph'
            'clefPosition'
            'clefTransposition'
            'clefTranspositionStyle'
            'createKeyOnClefChange'
            'createSpacing'
            'cueClefGlyph'
            'cueClefPosition'
            'cueClefTransposition'
            'cueClefTranspositionStyle'
            'currentCommandColumn'
            'currentMusicalColumn'
            'explicitClefVisibility'
            'explicitCueClefVisibility'
            'explicitKeySignatureVisibility'
            'extraNatural'
            'figuredBassAlterationDirection'
            'figuredBassCenterContinuations'
            'figuredBassFormatter'
            'fontSize'
            'forbidBreak'
            'forceClef'
            'harmonicAccidentals'
            'hasAxisGroup'
            'hasStaffSpacing'
            'ignoreFiguredBassRest'
            'implicitBassFigures'
            'initialTimeSignatureVisibility'
            'instrumentName'
            'internalBarNumber'
            'keepAliveInterfaces'
            'keyAlterationOrder'
            'keyAlterations'
            'lastKeyAlterations'
            'localAlterations'
            'middleCClefPosition'
            'middleCCuePosition'
            'middleCOffset'
            'ottavation'
            'partialBusy'
            'pedalSostenutoStrings'
            'pedalSostenutoStyle'
            'pedalSustainStrings'
            'pedalSustainStyle'
            'pedalUnaCordaStrings'
            'pedalUnaCordaStyle'
            'printKeyCancellation'
            'shortInstrumentName'
            'shortVocalName'
            'stavesFound'
            'timeSignatureFraction'
            'tonic'
            'useBassFigureExtenders'
            'vocalName'
            'whichBar'

        """
        property_names: typing.Set[str] = set()
        for engraver in self.engravers:
            property_names.update(engraver.property_names)
        return tuple(sorted(property_names))

    ### PUBLIC METHODS ###

    @staticmethod
    def list_all_contexts() -> tuple["LilyPondContext", ...]:
        r"""
        Lists all contexts.

        ..  container:: example

            >>> for lilypond_context in abjad.LilyPondContext.list_all_contexts():
            ...     lilypond_context
            ...
            LilyPondContext(name='ChoirStaff')
            LilyPondContext(name='ChordNames')
            LilyPondContext(name='CueVoice')
            LilyPondContext(name='Devnull')
            LilyPondContext(name='DrumStaff')
            LilyPondContext(name='DrumVoice')
            LilyPondContext(name='Dynamics')
            LilyPondContext(name='FiguredBass')
            LilyPondContext(name='FretBoards')
            LilyPondContext(name='Global')
            LilyPondContext(name='GrandStaff')
            LilyPondContext(name='GregorianTranscriptionStaff')
            LilyPondContext(name='GregorianTranscriptionVoice')
            LilyPondContext(name='KievanStaff')
            LilyPondContext(name='KievanVoice')
            LilyPondContext(name='Lyrics')
            LilyPondContext(name='MensuralStaff')
            LilyPondContext(name='MensuralVoice')
            LilyPondContext(name='NoteNames')
            LilyPondContext(name='NullVoice')
            LilyPondContext(name='OneStaff')
            LilyPondContext(name='PetrucciStaff')
            LilyPondContext(name='PetrucciVoice')
            LilyPondContext(name='PianoStaff')
            LilyPondContext(name='RhythmicStaff')
            LilyPondContext(name='Score')
            LilyPondContext(name='Staff')
            LilyPondContext(name='StaffGroup')
            LilyPondContext(name='TabStaff')
            LilyPondContext(name='TabVoice')
            LilyPondContext(name='VaticanaStaff')
            LilyPondContext(name='VaticanaVoice')
            LilyPondContext(name='Voice')

        """
        return tuple(LilyPondContext(name=name) for name in sorted(_lyenv.contexts))

    @classmethod
    def register(
        class_,
        accepted_by: list[str] | None = None,
        accepts=None,
        alias: typing.Union[str, "LilyPondContext"] | None = None,
        consists=None,
        default_child=None,
        denies=None,
        name: str | None = None,
        removes: list[str] | None = None,
    ) -> "LilyPondContext":
        r"""
        Registers a new context.

        ..  container:: example

            >>> custom_context = abjad.LilyPondContext.register(
            ...     accepted_by=['Score', 'StaffGroup'],
            ...     alias='Staff',
            ...     name='BowingStaff',
            ...     removes=['Note_heads_engraver'],
            ...     )
            >>> custom_context
            LilyPondContext(name='BowingStaff')

            >>> custom_context.is_custom
            True

            >>> for engraver in custom_context.engravers:
            ...     engraver
            ...
            LilyPondEngraver(name='Accidental_engraver')
            LilyPondEngraver(name='Axis_group_engraver')
            LilyPondEngraver(name='Bar_engraver')
            LilyPondEngraver(name='Clef_engraver')
            LilyPondEngraver(name='Collision_engraver')
            LilyPondEngraver(name='Cue_clef_engraver')
            LilyPondEngraver(name='Dot_column_engraver')
            LilyPondEngraver(name='Figured_bass_engraver')
            LilyPondEngraver(name='Figured_bass_position_engraver')
            LilyPondEngraver(name='Fingering_column_engraver')
            LilyPondEngraver(name='Font_size_engraver')
            LilyPondEngraver(name='Grob_pq_engraver')
            LilyPondEngraver(name='Instrument_name_engraver')
            LilyPondEngraver(name='Key_engraver')
            LilyPondEngraver(name='Ledger_line_engraver')
            LilyPondEngraver(name='Ottava_spanner_engraver')
            LilyPondEngraver(name='Output_property_engraver')
            LilyPondEngraver(name='Piano_pedal_align_engraver')
            LilyPondEngraver(name='Piano_pedal_engraver')
            LilyPondEngraver(name='Pure_from_neighbor_engraver')
            LilyPondEngraver(name='Rest_collision_engraver')
            LilyPondEngraver(name='Script_row_engraver')
            LilyPondEngraver(name='Separating_line_group_engraver')
            LilyPondEngraver(name='Staff_collecting_engraver')
            LilyPondEngraver(name='Staff_symbol_engraver')
            LilyPondEngraver(name='Time_signature_engraver')

            >>> score_context = abjad.LilyPondContext('Score')
            >>> custom_context in score_context.accepts
            True

            >>> custom_context.unregister()

        """
        assert name not in _lyenv.contexts
        context_entry: dict = {}
        context_entry["accepts"] = set()
        context_entry["consists"] = set()
        context_entry["is_custom"] = True
        if alias is not None:
            if not isinstance(alias, class_):
                alias_ = class_(name=alias)
            else:
                alias_ = alias
            assert isinstance(alias_, class_)
            context_entry["accepts"].update(_.name for _ in alias_.accepts)
            context_entry["consists"].update(_.name for _ in alias_.engravers)
            context_entry["aliases"] = set([alias_.name])
        if accepts:
            for x in accepts:
                if not isinstance(x, class_):
                    x = class_(name=x)
                assert isinstance(x, class_)
                context_entry["accepts"].add(x.name)
        if denies:
            for x in denies:
                if not isinstance(x, class_):
                    x = class_(name=x)
                assert isinstance(x, class_)
                if x.name in context_entry["accepts"]:
                    context_entry["accepts"].remove(x.name)
        if consists:
            for x in consists:
                if not isinstance(x, LilyPondEngraver):
                    x = LilyPondEngraver(name=x)
                assert isinstance(x, LilyPondEngraver)
                context_entry["consists"].add(x.name)
        if removes:
            for x in removes:
                if not isinstance(x, LilyPondEngraver):
                    x = LilyPondEngraver(name=x)
                assert isinstance(x, LilyPondEngraver)
                if x.name in context_entry["consists"]:
                    context_entry["consists"].remove(x.name)
        if default_child is not None:
            if not isinstance(default_child, class_):
                default_child = class_(name=default_child)
            assert isinstance(default_child, class_)
            context_entry["default_child"] = default_child.name
        accepting_contexts = set()
        if accepted_by:
            for x in accepted_by:
                if not isinstance(x, class_):
                    x = class_(name=x)
                assert isinstance(x, class_)
                accepting_contexts.add(x.name)
        assert isinstance(name, str)
        _lyenv.contexts[name] = context_entry
        for accepting_context in accepting_contexts:
            dictionary = _lyenv.contexts[accepting_context]
            assert isinstance(dictionary, dict)
            dictionary["accepts"].add(name)
        custom_context = class_(name=name)
        return custom_context

    def unregister(self, context=None) -> None:
        r"""
        Unregisters custom context.

        ..  container:: example

            >>> custom_context = abjad.LilyPondContext.register(
            ...     accepted_by=['Score', 'StaffGroup'],
            ...     alias='Staff',
            ...     name='FingeringStaff',
            ...     )

            >>> score_context = abjad.LilyPondContext('Score')
            >>> for accepted_context in score_context.accepts:
            ...     accepted_context
            ...
            LilyPondContext(name='ChoirStaff')
            LilyPondContext(name='ChordNames')
            LilyPondContext(name='Devnull')
            LilyPondContext(name='DrumStaff')
            LilyPondContext(name='Dynamics')
            LilyPondContext(name='FiguredBass')
            LilyPondContext(name='FingeringStaff')
            LilyPondContext(name='FretBoards')
            LilyPondContext(name='GrandStaff')
            LilyPondContext(name='GregorianTranscriptionStaff')
            LilyPondContext(name='KievanStaff')
            LilyPondContext(name='Lyrics')
            LilyPondContext(name='MensuralStaff')
            LilyPondContext(name='NoteNames')
            LilyPondContext(name='OneStaff')
            LilyPondContext(name='PetrucciStaff')
            LilyPondContext(name='PianoStaff')
            LilyPondContext(name='RhythmicStaff')
            LilyPondContext(name='Staff')
            LilyPondContext(name='StaffGroup')
            LilyPondContext(name='TabStaff')
            LilyPondContext(name='VaticanaStaff')

            >>> custom_context.unregister()

            >>> score_context = abjad.LilyPondContext('Score')
            >>> for accepted_context in score_context.accepts:
            ...     accepted_context
            ...
            LilyPondContext(name='ChoirStaff')
            LilyPondContext(name='ChordNames')
            LilyPondContext(name='Devnull')
            LilyPondContext(name='DrumStaff')
            LilyPondContext(name='Dynamics')
            LilyPondContext(name='FiguredBass')
            LilyPondContext(name='FretBoards')
            LilyPondContext(name='GrandStaff')
            LilyPondContext(name='GregorianTranscriptionStaff')
            LilyPondContext(name='KievanStaff')
            LilyPondContext(name='Lyrics')
            LilyPondContext(name='MensuralStaff')
            LilyPondContext(name='NoteNames')
            LilyPondContext(name='OneStaff')
            LilyPondContext(name='PetrucciStaff')
            LilyPondContext(name='PianoStaff')
            LilyPondContext(name='RhythmicStaff')
            LilyPondContext(name='Staff')
            LilyPondContext(name='StaffGroup')
            LilyPondContext(name='TabStaff')
            LilyPondContext(name='VaticanaStaff')

        """
        assert self.is_custom
        del _lyenv.contexts[self.name]
        del self._identity_map[self.name]
        for lilypond_type, context_info in _lyenv.contexts.items():
            assert isinstance(context_info, dict), repr(context_info)
            set_ = context_info["accepts"]
            assert isinstance(set_, set), repr(set_)
            if self.name in set_:
                set_.remove(self.name)


class LilyPondEngraver:
    """
    LilyPond engraver.

    ..  container:: example

        >>> abjad.LilyPondEngraver('Auto_beam_engraver')
        LilyPondEngraver(name='Auto_beam_engraver')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_name",)

    _identity_map: dict[str, "LilyPondEngraver"] = {}

    ### CONSTRUCTOR ###

    def __new__(class_, name="Note_heads_engraver"):
        if name in class_._identity_map:
            obj = class_._identity_map[name]
        else:
            obj = object.__new__(class_)
            class_._identity_map[name] = obj
        return obj

    ### INITIALIZER ###

    def __init__(self, name: str = "Note_heads_engraver") -> None:
        assert name in _lyenv.engravers
        self._name = name

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(name={self.name!r})"

    ### PUBLIC METHODS ###

    @staticmethod
    def list_all_engravers() -> tuple["LilyPondEngraver", ...]:
        """
        Lists all engravers.

        ..  container:: example

            >>> for lilypond_engraver in abjad.LilyPondEngraver.list_all_engravers():
            ...     lilypond_engraver
            ...
            LilyPondEngraver(name='Accidental_engraver')
            LilyPondEngraver(name='Ambitus_engraver')
            LilyPondEngraver(name='Arpeggio_engraver')
            LilyPondEngraver(name='Auto_beam_engraver')
            LilyPondEngraver(name='Axis_group_engraver')
            LilyPondEngraver(name='Balloon_engraver')
            LilyPondEngraver(name='Bar_engraver')
            LilyPondEngraver(name='Bar_number_engraver')
            LilyPondEngraver(name='Beam_collision_engraver')
            LilyPondEngraver(name='Beam_engraver')
            LilyPondEngraver(name='Beam_performer')
            LilyPondEngraver(name='Bend_engraver')
            LilyPondEngraver(name='Break_align_engraver')
            LilyPondEngraver(name='Breathing_sign_engraver')
            LilyPondEngraver(name='Chord_name_engraver')
            LilyPondEngraver(name='Chord_tremolo_engraver')
            LilyPondEngraver(name='Clef_engraver')
            LilyPondEngraver(name='Cluster_spanner_engraver')
            LilyPondEngraver(name='Collision_engraver')
            LilyPondEngraver(name='Completion_heads_engraver')
            LilyPondEngraver(name='Completion_rest_engraver')
            LilyPondEngraver(name='Concurrent_hairpin_engraver')
            LilyPondEngraver(name='Control_track_performer')
            LilyPondEngraver(name='Cue_clef_engraver')
            LilyPondEngraver(name='Custos_engraver')
            LilyPondEngraver(name='Default_bar_line_engraver')
            LilyPondEngraver(name='Dot_column_engraver')
            LilyPondEngraver(name='Dots_engraver')
            LilyPondEngraver(name='Double_percent_repeat_engraver')
            LilyPondEngraver(name='Drum_note_performer')
            LilyPondEngraver(name='Drum_notes_engraver')
            LilyPondEngraver(name='Dynamic_align_engraver')
            LilyPondEngraver(name='Dynamic_engraver')
            LilyPondEngraver(name='Dynamic_performer')
            LilyPondEngraver(name='Episema_engraver')
            LilyPondEngraver(name='Extender_engraver')
            LilyPondEngraver(name='Figured_bass_engraver')
            LilyPondEngraver(name='Figured_bass_position_engraver')
            LilyPondEngraver(name='Fingering_column_engraver')
            LilyPondEngraver(name='Fingering_engraver')
            LilyPondEngraver(name='Font_size_engraver')
            LilyPondEngraver(name='Footnote_engraver')
            LilyPondEngraver(name='Forbid_line_break_engraver')
            LilyPondEngraver(name='Fretboard_engraver')
            LilyPondEngraver(name='Glissando_engraver')
            LilyPondEngraver(name='Grace_auto_beam_engraver')
            LilyPondEngraver(name='Grace_beam_engraver')
            LilyPondEngraver(name='Grace_engraver')
            LilyPondEngraver(name='Grace_spacing_engraver')
            LilyPondEngraver(name='Grid_line_span_engraver')
            LilyPondEngraver(name='Grid_point_engraver')
            LilyPondEngraver(name='Grob_pq_engraver')
            LilyPondEngraver(name='Horizontal_bracket_engraver')
            LilyPondEngraver(name='Hyphen_engraver')
            LilyPondEngraver(name='Instrument_name_engraver')
            LilyPondEngraver(name='Instrument_switch_engraver')
            LilyPondEngraver(name='Keep_alive_together_engraver')
            LilyPondEngraver(name='Key_engraver')
            LilyPondEngraver(name='Key_performer')
            LilyPondEngraver(name='Kievan_ligature_engraver')
            LilyPondEngraver(name='Laissez_vibrer_engraver')
            LilyPondEngraver(name='Ledger_line_engraver')
            LilyPondEngraver(name='Ligature_bracket_engraver')
            LilyPondEngraver(name='Lyric_engraver')
            LilyPondEngraver(name='Lyric_performer')
            LilyPondEngraver(name='Mark_engraver')
            LilyPondEngraver(name='Measure_counter_engraver')
            LilyPondEngraver(name='Measure_grouping_engraver')
            LilyPondEngraver(name='Melody_engraver')
            LilyPondEngraver(name='Mensural_ligature_engraver')
            LilyPondEngraver(name='Merge_rests_engraver')
            LilyPondEngraver(name='Metronome_mark_engraver')
            LilyPondEngraver(name='Midi_control_change_performer')
            LilyPondEngraver(name='Multi_measure_rest_engraver')
            LilyPondEngraver(name='New_fingering_engraver')
            LilyPondEngraver(name='Note_head_line_engraver')
            LilyPondEngraver(name='Note_heads_engraver')
            LilyPondEngraver(name='Note_name_engraver')
            LilyPondEngraver(name='Note_performer')
            LilyPondEngraver(name='Note_spacing_engraver')
            LilyPondEngraver(name='Ottava_spanner_engraver')
            LilyPondEngraver(name='Output_property_engraver')
            LilyPondEngraver(name='Page_turn_engraver')
            LilyPondEngraver(name='Paper_column_engraver')
            LilyPondEngraver(name='Parenthesis_engraver')
            LilyPondEngraver(name='Part_combine_engraver')
            LilyPondEngraver(name='Percent_repeat_engraver')
            LilyPondEngraver(name='Phrasing_slur_engraver')
            LilyPondEngraver(name='Piano_pedal_align_engraver')
            LilyPondEngraver(name='Piano_pedal_engraver')
            LilyPondEngraver(name='Piano_pedal_performer')
            LilyPondEngraver(name='Pitch_squash_engraver')
            LilyPondEngraver(name='Pitched_trill_engraver')
            LilyPondEngraver(name='Pure_from_neighbor_engraver')
            LilyPondEngraver(name='Repeat_acknowledge_engraver')
            LilyPondEngraver(name='Repeat_tie_engraver')
            LilyPondEngraver(name='Rest_collision_engraver')
            LilyPondEngraver(name='Rest_engraver')
            LilyPondEngraver(name='Rhythmic_column_engraver')
            LilyPondEngraver(name='Script_column_engraver')
            LilyPondEngraver(name='Script_engraver')
            LilyPondEngraver(name='Script_row_engraver')
            LilyPondEngraver(name='Separating_line_group_engraver')
            LilyPondEngraver(name='Slash_repeat_engraver')
            LilyPondEngraver(name='Slur_engraver')
            LilyPondEngraver(name='Slur_performer')
            LilyPondEngraver(name='Spacing_engraver')
            LilyPondEngraver(name='Span_arpeggio_engraver')
            LilyPondEngraver(name='Span_bar_engraver')
            LilyPondEngraver(name='Span_bar_stub_engraver')
            LilyPondEngraver(name='Span_stem_engraver')
            LilyPondEngraver(name='Spanner_break_forbid_engraver')
            LilyPondEngraver(name='Staff_collecting_engraver')
            LilyPondEngraver(name='Staff_performer')
            LilyPondEngraver(name='Staff_symbol_engraver')
            LilyPondEngraver(name='Stanza_number_align_engraver')
            LilyPondEngraver(name='Stanza_number_engraver')
            LilyPondEngraver(name='Stem_engraver')
            LilyPondEngraver(name='System_start_delimiter_engraver')
            LilyPondEngraver(name='Tab_note_heads_engraver')
            LilyPondEngraver(name='Tab_staff_symbol_engraver')
            LilyPondEngraver(name='Tab_tie_follow_engraver')
            LilyPondEngraver(name='Tempo_performer')
            LilyPondEngraver(name='Text_engraver')
            LilyPondEngraver(name='Text_spanner_engraver')
            LilyPondEngraver(name='Tie_engraver')
            LilyPondEngraver(name='Tie_performer')
            LilyPondEngraver(name='Time_signature_engraver')
            LilyPondEngraver(name='Time_signature_performer')
            LilyPondEngraver(name='Timing_translator')
            LilyPondEngraver(name='Trill_spanner_engraver')
            LilyPondEngraver(name='Tuplet_engraver')
            LilyPondEngraver(name='Tweak_engraver')
            LilyPondEngraver(name='Vaticana_ligature_engraver')
            LilyPondEngraver(name='Vertical_align_engraver')
            LilyPondEngraver(name='Volta_engraver')

        """
        return tuple(LilyPondEngraver(name=name) for name in sorted(_lyenv.engravers))

    ### PUBLIC PROPERTIES ###

    @property
    def grobs(self) -> tuple["LilyPondGrob", ...]:
        """
        Gets LilyPond engraver's created grobs.

        ..  container:: example

            >>> engraver = abjad.LilyPondEngraver('Auto_beam_engraver')
            >>> for grob in engraver.grobs:
            ...     grob
            ...
            LilyPondGrob(name='Beam')

        """
        dictionary = _lyenv.engravers[self.name]
        assert isinstance(dictionary, dict), repr(dictionary)
        return tuple(LilyPondGrob(name=name) for name in dictionary["grobs_created"])

    @property
    def name(self) -> str:
        """
        Gets name of LilyPond engraver.

        ..  container:: example

            >>> engraver = abjad.LilyPondEngraver('Auto_beam_engraver')
            >>> engraver.name
            'Auto_beam_engraver'

        """
        return self._name

    @property
    def property_names(self) -> tuple[str, ...]:
        """
        Gets LilyPond engraver's property names.

        ..  container:: example

            >>> engraver = abjad.LilyPondEngraver('Auto_beam_engraver')
            >>> for property_name in engraver.property_names:
            ...     property_name
            ...
            'autoBeaming'
            'baseMoment'
            'beamExceptions'
            'beamHalfMeasure'
            'beatStructure'
            'subdivideBeams'

        """
        dictionary = _lyenv.engravers[self.name]
        assert isinstance(dictionary, dict), repr(dictionary)
        property_names: typing.Set[str] = set()
        property_names.update(dictionary["properties_read"])
        property_names.update(dictionary["properties_written"])
        return tuple(sorted(property_names))


class LilyPondGrob:
    """
    LilyPond grob.

    ..  container:: example

        >>> abjad.LilyPondGrob('Beam')
        LilyPondGrob(name='Beam')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_name",)

    _identity_map: dict[str, "LilyPondGrob"] = {}

    ### CONSTRUCTOR ###

    def __new__(class_, name="NoteHead"):
        if name in class_._identity_map:
            obj = class_._identity_map[name]
        else:
            obj = object.__new__(class_)
            class_._identity_map[name] = obj
        return obj

    ### INITIALIZER ###

    def __init__(self, name="NoteHead") -> None:
        assert name in _lyenv.grob_interfaces
        self._name = name

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(name={self.name!r})"

    ### PUBLIC PROPERTIES ###

    @property
    def interfaces(self) -> tuple["LilyPondGrobInterface", ...]:
        """
        Gets interfaces of LilyPond grob.

        ..  container:: example

            >>> grob = abjad.LilyPondGrob('Beam')
            >>> for interface in grob.interfaces:
            ...     interface
            ...
            LilyPondGrobInterface(name='beam-interface')
            LilyPondGrobInterface(name='font-interface')
            LilyPondGrobInterface(name='grob-interface')
            LilyPondGrobInterface(name='spanner-interface')
            LilyPondGrobInterface(name='staff-symbol-referencer-interface')
            LilyPondGrobInterface(name='unbreakable-spanner-interface')

        """
        return tuple(
            LilyPondGrobInterface(_) for _ in sorted(_lyenv.grob_interfaces[self.name])
        )

    @property
    def name(self) -> str:
        """
        Gets name of LilyPond grob.

        ..  container:: example

            >>> grob = abjad.LilyPondGrob('Beam')
            >>> grob.name
            'Beam'

        """
        return self._name

    @property
    def property_names(self) -> tuple[str, ...]:
        """
        Gets property names of LilyPond grob.

        ..  container:: example

            >>> grob = abjad.LilyPondGrob('Beam')
            >>> for property_name in grob.property_names:
            ...     property_name
            ...
            'X-extent'
            'X-offset'
            'X-positions'
            'Y-extent'
            'Y-offset'
            'after-line-breaking'
            'annotation'
            'auto-knee-gap'
            'avoid-slur'
            'beam-thickness'
            'beamed-stem-shorten'
            'beaming'
            'before-line-breaking'
            'break-overshoot'
            'breakable'
            'clip-edges'
            'collision-interfaces'
            'collision-voice-only'
            'color'
            'concaveness'
            'cross-staff'
            'damping'
            'details'
            'direction'
            'extra-offset'
            'font-encoding'
            'font-family'
            'font-features'
            'font-name'
            'font-series'
            'font-shape'
            'font-size'
            'footnote-music'
            'forced-spacing'
            'gap'
            'gap-count'
            'grow-direction'
            'horizontal-skylines'
            'id'
            'inspect-quants'
            'knee'
            'layer'
            'length-fraction'
            'minimum-X-extent'
            'minimum-Y-extent'
            'minimum-length'
            'minimum-length-after-break'
            'neutral-direction'
            'normalized-endpoints'
            'output-attributes'
            'parenthesis-friends'
            'positions'
            'rotation'
            'skip-quanting'
            'skyline-horizontal-padding'
            'spanner-id'
            'springs-and-rods'
            'staff-position'
            'stencil'
            'to-barline'
            'transparent'
            'vertical-skylines'
            'whiteout'
            'whiteout-style'

        """
        property_names: typing.Set[str] = set()
        for interface in self.interfaces:
            property_names.update(interface.property_names)
        return tuple(sorted(property_names))

    ### PUBLIC METHODS ###

    @staticmethod
    def list_all_grobs() -> tuple["LilyPondGrob", ...]:
        """
        Lists all grobs.

        ..  container:: example

            >>> for lilypond_grob in abjad.LilyPondGrob.list_all_grobs():
            ...     lilypond_grob
            ...
            LilyPondGrob(name='Accidental')
            LilyPondGrob(name='AccidentalCautionary')
            LilyPondGrob(name='AccidentalPlacement')
            LilyPondGrob(name='AccidentalSuggestion')
            LilyPondGrob(name='Ambitus')
            LilyPondGrob(name='AmbitusAccidental')
            LilyPondGrob(name='AmbitusLine')
            LilyPondGrob(name='AmbitusNoteHead')
            LilyPondGrob(name='Arpeggio')
            LilyPondGrob(name='BalloonTextItem')
            LilyPondGrob(name='BarLine')
            LilyPondGrob(name='BarNumber')
            LilyPondGrob(name='BassFigure')
            LilyPondGrob(name='BassFigureAlignment')
            LilyPondGrob(name='BassFigureAlignmentPositioning')
            LilyPondGrob(name='BassFigureBracket')
            LilyPondGrob(name='BassFigureContinuation')
            LilyPondGrob(name='BassFigureLine')
            LilyPondGrob(name='Beam')
            LilyPondGrob(name='BendAfter')
            LilyPondGrob(name='BreakAlignGroup')
            LilyPondGrob(name='BreakAlignment')
            LilyPondGrob(name='BreathingSign')
            LilyPondGrob(name='ChordName')
            LilyPondGrob(name='Clef')
            LilyPondGrob(name='ClefModifier')
            LilyPondGrob(name='ClusterSpanner')
            LilyPondGrob(name='ClusterSpannerBeacon')
            LilyPondGrob(name='CombineTextScript')
            LilyPondGrob(name='CueClef')
            LilyPondGrob(name='CueEndClef')
            LilyPondGrob(name='Custos')
            LilyPondGrob(name='DotColumn')
            LilyPondGrob(name='Dots')
            LilyPondGrob(name='DoublePercentRepeat')
            LilyPondGrob(name='DoublePercentRepeatCounter')
            LilyPondGrob(name='DoubleRepeatSlash')
            LilyPondGrob(name='DynamicLineSpanner')
            LilyPondGrob(name='DynamicText')
            LilyPondGrob(name='DynamicTextSpanner')
            LilyPondGrob(name='Episema')
            LilyPondGrob(name='Fingering')
            LilyPondGrob(name='FingeringColumn')
            LilyPondGrob(name='Flag')
            LilyPondGrob(name='FootnoteItem')
            LilyPondGrob(name='FootnoteSpanner')
            LilyPondGrob(name='FretBoard')
            LilyPondGrob(name='Glissando')
            LilyPondGrob(name='GraceSpacing')
            LilyPondGrob(name='GridLine')
            LilyPondGrob(name='GridPoint')
            LilyPondGrob(name='Hairpin')
            LilyPondGrob(name='HorizontalBracket')
            LilyPondGrob(name='HorizontalBracketText')
            LilyPondGrob(name='InstrumentName')
            LilyPondGrob(name='InstrumentSwitch')
            LilyPondGrob(name='KeyCancellation')
            LilyPondGrob(name='KeySignature')
            LilyPondGrob(name='KievanLigature')
            LilyPondGrob(name='LaissezVibrerTie')
            LilyPondGrob(name='LaissezVibrerTieColumn')
            LilyPondGrob(name='LedgerLineSpanner')
            LilyPondGrob(name='LeftEdge')
            LilyPondGrob(name='LigatureBracket')
            LilyPondGrob(name='LyricExtender')
            LilyPondGrob(name='LyricHyphen')
            LilyPondGrob(name='LyricSpace')
            LilyPondGrob(name='LyricText')
            LilyPondGrob(name='MeasureCounter')
            LilyPondGrob(name='MeasureGrouping')
            LilyPondGrob(name='MelodyItem')
            LilyPondGrob(name='MensuralLigature')
            LilyPondGrob(name='MetronomeMark')
            LilyPondGrob(name='MultiMeasureRest')
            LilyPondGrob(name='MultiMeasureRestNumber')
            LilyPondGrob(name='MultiMeasureRestText')
            LilyPondGrob(name='NonMusicalPaperColumn')
            LilyPondGrob(name='NoteCollision')
            LilyPondGrob(name='NoteColumn')
            LilyPondGrob(name='NoteHead')
            LilyPondGrob(name='NoteName')
            LilyPondGrob(name='NoteSpacing')
            LilyPondGrob(name='OttavaBracket')
            LilyPondGrob(name='PaperColumn')
            LilyPondGrob(name='ParenthesesItem')
            LilyPondGrob(name='PercentRepeat')
            LilyPondGrob(name='PercentRepeatCounter')
            LilyPondGrob(name='PhrasingSlur')
            LilyPondGrob(name='PianoPedalBracket')
            LilyPondGrob(name='RehearsalMark')
            LilyPondGrob(name='RepeatSlash')
            LilyPondGrob(name='RepeatTie')
            LilyPondGrob(name='RepeatTieColumn')
            LilyPondGrob(name='Rest')
            LilyPondGrob(name='RestCollision')
            LilyPondGrob(name='Script')
            LilyPondGrob(name='ScriptColumn')
            LilyPondGrob(name='ScriptRow')
            LilyPondGrob(name='Slur')
            LilyPondGrob(name='SostenutoPedal')
            LilyPondGrob(name='SostenutoPedalLineSpanner')
            LilyPondGrob(name='SpacingSpanner')
            LilyPondGrob(name='SpanBar')
            LilyPondGrob(name='SpanBarStub')
            LilyPondGrob(name='StaffGrouper')
            LilyPondGrob(name='StaffSpacing')
            LilyPondGrob(name='StaffSymbol')
            LilyPondGrob(name='StanzaNumber')
            LilyPondGrob(name='Stem')
            LilyPondGrob(name='StemStub')
            LilyPondGrob(name='StemTremolo')
            LilyPondGrob(name='StringNumber')
            LilyPondGrob(name='StrokeFinger')
            LilyPondGrob(name='SustainPedal')
            LilyPondGrob(name='SustainPedalLineSpanner')
            LilyPondGrob(name='System')
            LilyPondGrob(name='SystemStartBar')
            LilyPondGrob(name='SystemStartBrace')
            LilyPondGrob(name='SystemStartBracket')
            LilyPondGrob(name='SystemStartSquare')
            LilyPondGrob(name='TabNoteHead')
            LilyPondGrob(name='TextScript')
            LilyPondGrob(name='TextSpanner')
            LilyPondGrob(name='Tie')
            LilyPondGrob(name='TieColumn')
            LilyPondGrob(name='TimeSignature')
            LilyPondGrob(name='TrillPitchAccidental')
            LilyPondGrob(name='TrillPitchGroup')
            LilyPondGrob(name='TrillPitchHead')
            LilyPondGrob(name='TrillSpanner')
            LilyPondGrob(name='TupletBracket')
            LilyPondGrob(name='TupletNumber')
            LilyPondGrob(name='UnaCordaPedal')
            LilyPondGrob(name='UnaCordaPedalLineSpanner')
            LilyPondGrob(name='VaticanaLigature')
            LilyPondGrob(name='Vertical')
            LilyPondGrob(name='VerticalAxisGroup')
            LilyPondGrob(name='VoiceFollower')
            LilyPondGrob(name='VoltaBracket')
            LilyPondGrob(name='VoltaBracketSpanner')

        """
        return tuple(LilyPondGrob(name) for name in sorted(_lyenv.grob_interfaces))


class LilyPondGrobInterface:
    """
    LilyPond grob interface.

    ..  container:: example

        >>> abjad.LilyPondGrobInterface('beam-interface')
        LilyPondGrobInterface(name='beam-interface')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_name",)

    _identity_map: dict[str, "LilyPondGrobInterface"] = {}

    ### CONSTRUCTOR ###

    def __new__(class_, name="grob-interface"):
        if name in class_._identity_map:
            obj = class_._identity_map[name]
        else:
            obj = object.__new__(class_)
            class_._identity_map[name] = obj
        return obj

    ### INITIALIZER ###

    def __init__(self, name: str = "grob-interface") -> None:
        assert name in _lyenv.interface_properties
        self._name = name

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(name={self.name!r})"

    ### PUBLIC METHODS ###

    @staticmethod
    def list_all_interfaces() -> tuple["LilyPondGrobInterface", ...]:
        """
        Lists all interfaces.

        ..  container:: example

            >>> for grob_interface in abjad.LilyPondGrobInterface.list_all_interfaces():
            ...     grob_interface
            ...
            LilyPondGrobInterface(name='accidental-interface')
            LilyPondGrobInterface(name='accidental-placement-interface')
            LilyPondGrobInterface(name='accidental-suggestion-interface')
            LilyPondGrobInterface(name='align-interface')
            LilyPondGrobInterface(name='ambitus-interface')
            LilyPondGrobInterface(name='arpeggio-interface')
            LilyPondGrobInterface(name='axis-group-interface')
            LilyPondGrobInterface(name='balloon-interface')
            LilyPondGrobInterface(name='bar-line-interface')
            LilyPondGrobInterface(name='bass-figure-alignment-interface')
            LilyPondGrobInterface(name='bass-figure-interface')
            LilyPondGrobInterface(name='beam-interface')
            LilyPondGrobInterface(name='bend-after-interface')
            LilyPondGrobInterface(name='break-alignable-interface')
            LilyPondGrobInterface(name='break-aligned-interface')
            LilyPondGrobInterface(name='break-alignment-interface')
            LilyPondGrobInterface(name='breathing-sign-interface')
            LilyPondGrobInterface(name='chord-name-interface')
            LilyPondGrobInterface(name='clef-interface')
            LilyPondGrobInterface(name='clef-modifier-interface')
            LilyPondGrobInterface(name='cluster-beacon-interface')
            LilyPondGrobInterface(name='cluster-interface')
            LilyPondGrobInterface(name='custos-interface')
            LilyPondGrobInterface(name='dot-column-interface')
            LilyPondGrobInterface(name='dots-interface')
            LilyPondGrobInterface(name='dynamic-interface')
            LilyPondGrobInterface(name='dynamic-line-spanner-interface')
            LilyPondGrobInterface(name='dynamic-text-interface')
            LilyPondGrobInterface(name='dynamic-text-spanner-interface')
            LilyPondGrobInterface(name='enclosing-bracket-interface')
            LilyPondGrobInterface(name='episema-interface')
            LilyPondGrobInterface(name='figured-bass-continuation-interface')
            LilyPondGrobInterface(name='finger-interface')
            LilyPondGrobInterface(name='fingering-column-interface')
            LilyPondGrobInterface(name='flag-interface')
            LilyPondGrobInterface(name='font-interface')
            LilyPondGrobInterface(name='footnote-interface')
            LilyPondGrobInterface(name='footnote-spanner-interface')
            LilyPondGrobInterface(name='fret-diagram-interface')
            LilyPondGrobInterface(name='glissando-interface')
            LilyPondGrobInterface(name='grace-spacing-interface')
            LilyPondGrobInterface(name='gregorian-ligature-interface')
            LilyPondGrobInterface(name='grid-line-interface')
            LilyPondGrobInterface(name='grid-point-interface')
            LilyPondGrobInterface(name='grob-interface')
            LilyPondGrobInterface(name='hairpin-interface')
            LilyPondGrobInterface(name='hara-kiri-group-spanner-interface')
            LilyPondGrobInterface(name='horizontal-bracket-interface')
            LilyPondGrobInterface(name='horizontal-bracket-text-interface')
            LilyPondGrobInterface(name='inline-accidental-interface')
            LilyPondGrobInterface(name='instrument-specific-markup-interface')
            LilyPondGrobInterface(name='item-interface')
            LilyPondGrobInterface(name='key-cancellation-interface')
            LilyPondGrobInterface(name='key-signature-interface')
            LilyPondGrobInterface(name='kievan-ligature-interface')
            LilyPondGrobInterface(name='ledger-line-spanner-interface')
            LilyPondGrobInterface(name='ledgered-interface')
            LilyPondGrobInterface(name='ligature-bracket-interface')
            LilyPondGrobInterface(name='ligature-head-interface')
            LilyPondGrobInterface(name='ligature-interface')
            LilyPondGrobInterface(name='line-interface')
            LilyPondGrobInterface(name='line-spanner-interface')
            LilyPondGrobInterface(name='lyric-extender-interface')
            LilyPondGrobInterface(name='lyric-hyphen-interface')
            LilyPondGrobInterface(name='lyric-interface')
            LilyPondGrobInterface(name='lyric-syllable-interface')
            LilyPondGrobInterface(name='mark-interface')
            LilyPondGrobInterface(name='measure-counter-interface')
            LilyPondGrobInterface(name='measure-grouping-interface')
            LilyPondGrobInterface(name='melody-spanner-interface')
            LilyPondGrobInterface(name='mensural-ligature-interface')
            LilyPondGrobInterface(name='metronome-mark-interface')
            LilyPondGrobInterface(name='multi-measure-interface')
            LilyPondGrobInterface(name='multi-measure-rest-interface')
            LilyPondGrobInterface(name='note-collision-interface')
            LilyPondGrobInterface(name='note-column-interface')
            LilyPondGrobInterface(name='note-head-interface')
            LilyPondGrobInterface(name='note-name-interface')
            LilyPondGrobInterface(name='note-spacing-interface')
            LilyPondGrobInterface(name='number-interface')
            LilyPondGrobInterface(name='only-prebreak-interface')
            LilyPondGrobInterface(name='ottava-bracket-interface')
            LilyPondGrobInterface(name='outside-staff-axis-group-interface')
            LilyPondGrobInterface(name='outside-staff-interface')
            LilyPondGrobInterface(name='paper-column-interface')
            LilyPondGrobInterface(name='parentheses-interface')
            LilyPondGrobInterface(name='percent-repeat-interface')
            LilyPondGrobInterface(name='percent-repeat-item-interface')
            LilyPondGrobInterface(name='piano-pedal-bracket-interface')
            LilyPondGrobInterface(name='piano-pedal-interface')
            LilyPondGrobInterface(name='piano-pedal-script-interface')
            LilyPondGrobInterface(name='pitched-trill-interface')
            LilyPondGrobInterface(name='pure-from-neighbor-interface')
            LilyPondGrobInterface(name='rest-collision-interface')
            LilyPondGrobInterface(name='rest-interface')
            LilyPondGrobInterface(name='rhythmic-grob-interface')
            LilyPondGrobInterface(name='rhythmic-head-interface')
            LilyPondGrobInterface(name='script-column-interface')
            LilyPondGrobInterface(name='script-interface')
            LilyPondGrobInterface(name='self-alignment-interface')
            LilyPondGrobInterface(name='semi-tie-column-interface')
            LilyPondGrobInterface(name='semi-tie-interface')
            LilyPondGrobInterface(name='separation-item-interface')
            LilyPondGrobInterface(name='side-position-interface')
            LilyPondGrobInterface(name='slur-interface')
            LilyPondGrobInterface(name='spaceable-grob-interface')
            LilyPondGrobInterface(name='spacing-interface')
            LilyPondGrobInterface(name='spacing-options-interface')
            LilyPondGrobInterface(name='spacing-spanner-interface')
            LilyPondGrobInterface(name='span-bar-interface')
            LilyPondGrobInterface(name='spanner-interface')
            LilyPondGrobInterface(name='staff-grouper-interface')
            LilyPondGrobInterface(name='staff-spacing-interface')
            LilyPondGrobInterface(name='staff-symbol-interface')
            LilyPondGrobInterface(name='staff-symbol-referencer-interface')
            LilyPondGrobInterface(name='stanza-number-interface')
            LilyPondGrobInterface(name='stem-interface')
            LilyPondGrobInterface(name='stem-tremolo-interface')
            LilyPondGrobInterface(name='string-number-interface')
            LilyPondGrobInterface(name='stroke-finger-interface')
            LilyPondGrobInterface(name='system-interface')
            LilyPondGrobInterface(name='system-start-delimiter-interface')
            LilyPondGrobInterface(name='system-start-text-interface')
            LilyPondGrobInterface(name='tab-note-head-interface')
            LilyPondGrobInterface(name='text-interface')
            LilyPondGrobInterface(name='text-script-interface')
            LilyPondGrobInterface(name='tie-column-interface')
            LilyPondGrobInterface(name='tie-interface')
            LilyPondGrobInterface(name='time-signature-interface')
            LilyPondGrobInterface(name='trill-pitch-accidental-interface')
            LilyPondGrobInterface(name='trill-spanner-interface')
            LilyPondGrobInterface(name='tuplet-bracket-interface')
            LilyPondGrobInterface(name='tuplet-number-interface')
            LilyPondGrobInterface(name='unbreakable-spanner-interface')
            LilyPondGrobInterface(name='vaticana-ligature-interface')
            LilyPondGrobInterface(name='volta-bracket-interface')
            LilyPondGrobInterface(name='volta-interface')

        """
        return tuple(
            LilyPondGrobInterface(_) for _ in sorted(_lyenv.interface_properties)
        )

    ### PUBLIC PROPERTIES ###

    @property
    def name(self) -> str:
        """
        Gets name of LilyPond grob interface.

        ..  container:: example

            >>> interface = abjad.LilyPondGrobInterface('beam-interface')
            >>> interface.name
            'beam-interface'

        """
        return self._name

    @property
    def property_names(self) -> tuple[str, ...]:
        """
        Gets property names of LilyPond grob interface.

        ..  container:: example

            >>> interface = abjad.LilyPondGrobInterface('beam-interface')
            >>> for property_name in interface.property_names:
            ...     property_name
            ...
            'X-positions'
            'annotation'
            'auto-knee-gap'
            'beam-thickness'
            'beamed-stem-shorten'
            'beaming'
            'break-overshoot'
            'clip-edges'
            'collision-interfaces'
            'collision-voice-only'
            'concaveness'
            'damping'
            'details'
            'direction'
            'gap'
            'gap-count'
            'grow-direction'
            'inspect-quants'
            'knee'
            'length-fraction'
            'neutral-direction'
            'positions'
            'skip-quanting'

        """
        names = _lyenv.interface_properties[self.name]
        assert isinstance(names, list), repr(names)
        assert all(isinstance(_, str) for _ in names), repr(names)
        return tuple(names)
