# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class LilyPondContext(abctools.AbjadValueObject):
    r'''A LilyPond context.

    ::

        >>> context = lilypondnametools.LilyPondContext('MensuralStaff')
        >>> print(format(context))
        lilypondnametools.LilyPondContext(
            name='MensuralStaff',
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        )

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

    ### PUBLIC PROPERTIES ###

    @property
    def accepted_by(self):
        r'''Gets contexts accepting LilyPond context.

        ::

            >>> for accepting_context in context.accepted_by:
            ...     accepting_context
            ...
            LilyPondContext(name='Score')

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
            return LilyPondContext(name=alias)
        return None

    @property
    def default_child(self):
        r'''Gets default child of LilyPond context.

        ::

            >>> context.default_child
            LilyPondContext(name='MensuralVoice')

        Returns LilyPond context or none.
        '''
        from abjad.ly import contexts
        default_child = contexts[self.name].get('default_child', None)
        if default_child:
            return LilyPondContext(name=default_child)

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