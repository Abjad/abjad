# -*- coding: utf-8 -*-
from abjad.tools import abctools


class LilyPondContext(abctools.AbjadValueObject):
    r'''A LilyPond context.

    ::

        >>> context = lilypondnametools.LilyPondContext('MensuralStaff')
        >>> print(format(context))
        lilypondnametools.LilyPondContext(
            name='MensuralStaff',
            )

    ::

        >>> for lilypond_context in lilypondnametools.LilyPondContext.list_all_contexts():
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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        )

    _identity_map = {}

    ### CONSTRUCTOR ###

    def __new__(class_, name='Voice'):
        if isinstance(name, class_):
            name = name.name
        if name in class_._identity_map:
            obj = class_._identity_map[name]
        else:
            obj = object.__new__(class_)
            class_._identity_map[name] = obj
        return obj

    ### INITIALIZER ###

    def __init__(self, name='Voice'):
        from abjad.ly import contexts
        assert name in contexts
        self._name = name

    ### PUBLIC METHODS ###

    @staticmethod
    def list_all_contexts():
        r'''Lists all contexts.

        ::

            >>> for lilypond_context in lilypondnametools.LilyPondContext.list_all_contexts():
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

        Returns tuple.
        '''
        from abjad.ly import contexts
        return tuple(LilyPondContext(name=name) for name in sorted(contexts))

    @classmethod
    def register(
        class_,
        accepted_by=None,
        accepts=None,
        alias=None,
        consists=None,
        default_child=None,
        denies=None,
        name=None,
        removes=None,
        ):
        r'''Registers a new context.

        ::

            >>> custom_context = lilypondnametools.LilyPondContext.register(
            ...     accepted_by=['Score', 'StaffGroup'],
            ...     alias='Staff',
            ...     name='BowingStaff',
            ...     removes=['Note_heads_engraver'],
            ...     )
            >>> print(format(custom_context))
            lilypondnametools.LilyPondContext(
                name='BowingStaff',
                )

        ::

            >>> custom_context.is_custom
            True

        ::

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

        ::

            >>> score_context = lilypondnametools.LilyPondContext('Score')
            >>> custom_context in score_context.accepts
            True

        ::

            >>> custom_context.unregister()

        '''
        from abjad.ly import contexts
        from abjad.tools import lilypondnametools
        assert name not in contexts
        context_entry = {
            'accepts': set(),
            'consists': set(),
            'is_custom': True,
            }
        if alias is not None:
            if not isinstance(alias, class_):
                alias = class_(name=alias)
            assert isinstance(alias, class_)
            context_entry['accepts'].update(_.name for _ in alias.accepts)
            context_entry['consists'].update(_.name for _ in alias.engravers)
            context_entry['aliases'] = set([alias.name])
        if accepts:
            for x in accepts:
                if not isinstance(x, class_):
                    x = class_(name=x)
                assert isinstance(x, class_)
                context_entry['accepts'].add(x.name)
        if denies:
            for x in denies:
                if not isinstance(x, class_):
                    x = class_(name=x)
                assert isinstance(x, class_)
                if x.name in context_entry['accepts']:
                    context_entry['accepts'].remove(x.name)
        if consists:
            for x in consists:
                if not isinstance(x, lilypondnametools.LilyPondEngraver):
                    x = lilypondnametools.LilyPondEngraver(name=x)
                assert isinstance(x, lilypondnametools.LilyPondEngraver)
                context_entry['consists'].add(x.name)
        if removes:
            for x in removes:
                if not isinstance(x, lilypondnametools.LilyPondEngraver):
                    x = lilypondnametools.LilyPondEngraver(name=x)
                assert isinstance(x, lilypondnametools.LilyPondEngraver)
                if x.name in context_entry['consists']:
                    context_entry['consists'].remove(x.name)
        if default_child is not None:
            if not isinstance(default_child, class_):
                default_child = class_(name=default_child)
            assert isinstance(default_child, class_)
            context_entry['default_child'] = default_child.name
        accepting_contexts = set()
        if accepted_by:
            for x in accepted_by:
                if not isinstance(x, class_):
                    x = class_(name=x)
                assert isinstance(x, class_)
                accepting_contexts.add(x.name)
        contexts[name] = context_entry
        for accepting_context in accepting_contexts:
            contexts[accepting_context]['accepts'].add(name)
        custom_context = class_(name=name)
        return custom_context

    def unregister(
        self,
        context=None,
        ):
        r'''Unregisters custom context.

        ::

            >>> custom_context = lilypondnametools.LilyPondContext.register(
            ...     accepted_by=['Score', 'StaffGroup'],
            ...     alias='Staff',
            ...     name='FingeringStaff',
            ...     )

        ::

            >>> score_context = lilypondnametools.LilyPondContext('Score')
            >>> for accepted_context in score_context.accepts:
            ...     accepted_context
            ...
            LilyPondContext(name='ChoirStaff')
            LilyPondContext(name='ChordNames')
            LilyPondContext(name='Devnull')
            LilyPondContext(name='DrumStaff')
            LilyPondContext(name='FiguredBass')
            LilyPondContext(name='FingeringStaff')
            LilyPondContext(name='FretBoards')
            LilyPondContext(name='GrandStaff')
            LilyPondContext(name='GregorianTranscriptionStaff')
            LilyPondContext(name='KievanStaff')
            LilyPondContext(name='Lyrics')
            LilyPondContext(name='MensuralStaff')
            LilyPondContext(name='NoteNames')
            LilyPondContext(name='PetrucciStaff')
            LilyPondContext(name='PianoStaff')
            LilyPondContext(name='RhythmicStaff')
            LilyPondContext(name='Staff')
            LilyPondContext(name='StaffGroup')
            LilyPondContext(name='TabStaff')
            LilyPondContext(name='VaticanaStaff')

        ::

            >>> custom_context.unregister()

        ::

            >>> score_context = lilypondnametools.LilyPondContext('Score')
            >>> for accepted_context in score_context.accepts:
            ...     accepted_context
            ...
            LilyPondContext(name='ChoirStaff')
            LilyPondContext(name='ChordNames')
            LilyPondContext(name='Devnull')
            LilyPondContext(name='DrumStaff')
            LilyPondContext(name='FiguredBass')
            LilyPondContext(name='FretBoards')
            LilyPondContext(name='GrandStaff')
            LilyPondContext(name='GregorianTranscriptionStaff')
            LilyPondContext(name='KievanStaff')
            LilyPondContext(name='Lyrics')
            LilyPondContext(name='MensuralStaff')
            LilyPondContext(name='NoteNames')
            LilyPondContext(name='PetrucciStaff')
            LilyPondContext(name='PianoStaff')
            LilyPondContext(name='RhythmicStaff')
            LilyPondContext(name='Staff')
            LilyPondContext(name='StaffGroup')
            LilyPondContext(name='TabStaff')
            LilyPondContext(name='VaticanaStaff')

        '''
        from abjad.ly import contexts
        assert self.is_custom
        del(contexts[self.name])
        del(self._identity_map[self.name])
        for context_name, context_info in contexts.items():
            if self.name in context_info['accepts']:
                context_info['accepts'].remove(self.name)

    ### PUBLIC PROPERTIES ###

    @property
    def accepted_by(self):
        r'''Gets contexts accepting LilyPond context.

        ::

            >>> for accepting_context in context.accepted_by:
            ...     accepting_context
            ...
            LilyPondContext(name='Score')

        ::

            >>> for lilypond_context in lilypondnametools.LilyPondContext.list_all_contexts():
            ...     print('{}:'.format(lilypond_context.name))
            ...     accepted_by = lilypond_context.accepted_by
            ...     if accepted_by:
            ...         accepted_by = ',\n    '.join(_.name for _ in accepted_by)
            ...         print('    {}'.format(accepted_by))
            ...
            ChoirStaff:
                ChoirStaff,
                Score,
                StaffGroup
            ChordNames:
                ChoirStaff,
                GrandStaff,
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
                PianoStaff,
                Score,
                StaffGroup
            DrumVoice:
                DrumStaff
            Dynamics:
                GrandStaff,
                PianoStaff
            FiguredBass:
                ChoirStaff,
                GrandStaff,
                PianoStaff,
                Score,
                StaffGroup
            FretBoards:
                Score,
                StaffGroup
            Global:
            GrandStaff:
                ChoirStaff,
                Score,
                StaffGroup
            GregorianTranscriptionStaff:
                Score
            GregorianTranscriptionVoice:
                GregorianTranscriptionStaff
            KievanStaff:
                Score
            KievanVoice:
                KievanStaff
            Lyrics:
                ChoirStaff,
                GrandStaff,
                PianoStaff,
                Score,
                StaffGroup
            MensuralStaff:
                Score
            MensuralVoice:
                MensuralStaff
            NoteNames:
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
            PetrucciStaff:
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
                PianoStaff,
                Score,
                StaffGroup
            Score:
                Global
            Staff:
                ChoirStaff,
                GrandStaff,
                PianoStaff,
                Score,
                StaffGroup
            StaffGroup:
                ChoirStaff,
                Score,
                StaffGroup
            TabStaff:
                GrandStaff,
                PianoStaff,
                Score,
                StaffGroup
            TabVoice:
                TabStaff
            VaticanaStaff:
                Score
            VaticanaVoice:
                VaticanaStaff
            Voice:
                RhythmicStaff,
                Staff

        '''
        from abjad.ly import contexts
        accepting_contexts = set()
        for context_name, context_info in contexts.items():
            if self.name in context_info['accepts']:
                accepting_context = LilyPondContext(context_name)
                accepting_contexts.add(accepting_context)
        return tuple(sorted(accepting_contexts, key=lambda x: x.name))

    @property
    def accepts(self):
        r'''Gets contexts accepted by LilyPond context.

        ::

            >>> for accepted_context in context.accepts:
            ...     accepted_context
            ...
            LilyPondContext(name='CueVoice')
            LilyPondContext(name='MensuralVoice')
            LilyPondContext(name='NullVoice')

        Returns tuple.
        '''
        from abjad.ly import contexts
        accepts = (LilyPondContext(name=name)
            for name in contexts[self.name]['accepts'])
        return tuple(sorted(accepts, key=lambda x: x.name))

    @property
    def alias(self):
        r'''Gets alias of LilyPond context.

        ::

            >>> context.alias
            LilyPondContext(name='Staff')

        Returns LilyPond context or none.
        '''
        from abjad.ly import contexts
        aliases = contexts[self.name]['aliases']
        if aliases:
            alias = tuple(aliases)[0]
            if alias not in contexts:
                return None
            return LilyPondContext(name=alias)
        return None

    @property
    def default_child(self):
        r'''Gets default child of LilyPond context.

        ::

            >>> context.default_child
            LilyPondContext(name='MensuralVoice')

        ::

            >>> for lilypond_context in lilypondnametools.LilyPondContext.list_all_contexts():
            ...     print('{}:'.format(lilypond_context.name))
            ...     default_child = lilypond_context.default_child
            ...     if default_child:
            ...         print('    {}'.format(default_child.name))
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

        Returns LilyPond context or none.
        '''
        from abjad.ly import contexts
        if self.is_bottom_context:
            return None
        default_child_name = contexts[self.name].get('default_child', None)
        if default_child_name is None:
            alias = self.alias
            if alias is not None:
                return alias.default_child
        if default_child_name and default_child_name in contexts:
            return LilyPondContext(name=default_child_name)

    @property
    def engravers(self):
        r'''Gets engravers belonging to LilyPond context.

        ::

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

        Returns tuple.
        '''
        from abjad.ly import contexts
        from abjad.tools import lilypondnametools
        engravers = set()
        for engraver_name in contexts[self.name]['consists']:
            engraver = lilypondnametools.LilyPondEngraver(name=engraver_name)
            engravers.add(engraver)
        engravers = tuple(sorted(engravers, key=lambda x: x.name))
        return engravers

    @property
    def grobs(self):
        r'''Gets grobs created by LilyPond context.

        ::

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

        Returns tuple.
        '''
        grobs = set()
        for engraver in self.engravers:
            grobs.update(engraver.grobs)
        return tuple(sorted(grobs, key=lambda x: x.name))

    @property
    def is_bottom_context(self):
        r'''Is true if LilyPond context is a bottom context. Otherwise false.

        ::

            >>> for lilypond_context in lilypondnametools.LilyPondContext.list_all_contexts():
            ...     is_bottom_context = 'X' if lilypond_context.is_bottom_context else ' '
            ...     print('[{}] {}'.format(is_bottom_context, lilypond_context.name))
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

        Returns true or false.
        '''
        if not self.accepts:
            return True
        return False

    @property
    def is_custom(self):
        r'''Is true if LilyPond context is user-created. Otherwise false.

        ::

            >>> context.is_custom
            False

        Returns true or false.
        '''
        from abjad.ly import contexts
        return bool(contexts[self.name].get('is_custom', False))

    @property
    def is_global_context(self):
        r'''Is true if LilyPond context is a global context. Otherwise false.

        ::

            >>> for lilypond_context in lilypondnametools.LilyPondContext.list_all_contexts():
            ...     is_global_context = 'X' if lilypond_context.is_global_context else ' '
            ...     print('[{}] {}'.format(is_global_context, lilypond_context.name))
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

        Returns true or false.
        '''
        if not self.accepts:
            return False
        elif self is type(self)('Global'):
            return True
        elif self.alias is type(self)('Global'):
            return True
        return False

    @property
    def is_score_context(self):
        r'''Is true if LilyPond context is a score context. Otherwise false.

        ::

            >>> for lilypond_context in lilypondnametools.LilyPondContext.list_all_contexts():
            ...     is_score_context = 'X' if lilypond_context.is_score_context else ' '
            ...     print('[{}] {}'.format(is_score_context, lilypond_context.name))
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

        Returns true or false.
        '''
        if not self.accepts:
            return False
        elif self is type(self)('Score'):
            return True
        elif self.alias is type(self)('Score'):
            return True
        return False

    @property
    def is_staff_context(self):
        r'''Is true if LilyPond context is a staff context. Otherwise false.

        ::

            >>> for lilypond_context in lilypondnametools.LilyPondContext.list_all_contexts():
            ...     is_staff_context = 'X' if lilypond_context.is_staff_context else ' '
            ...     print('[{}] {}'.format(is_staff_context, lilypond_context.name))
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

        Returns true or false.
        '''
        if not self.accepts:
            return False
        elif self is type(self)('Staff'):
            return True
        elif self.alias is type(self)('Staff'):
            return True
        return False

    @property
    def is_staff_group_context(self):
        r'''Is true if LilyPond context is a staff group context. Otherwise false.

        ::

            >>> for lilypond_context in lilypondnametools.LilyPondContext.list_all_contexts():
            ...     is_staff_group_context = 'X' if lilypond_context.is_staff_group_context else ' '
            ...     print('[{}] {}'.format(is_staff_group_context, lilypond_context.name))
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

        Returns true or false.
        '''
        return not any([
            self.is_global_context,
            self.is_score_context,
            self.is_staff_context,
            self.is_bottom_context,
            ])

    @property
    def name(self):
        r'''Gets name of LilyPond context.

        ::

            >>> context.name
            'MensuralStaff'

        Returns string.
        '''
        return self._name

    @property
    def property_names(self):
        r'''Gets property names of LilyPond context.

        ::

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

        Returns tuple.
        '''
        property_names = set()
        for engraver in self.engravers:
            property_names.update(engraver.property_names)
        return tuple(sorted(property_names))
