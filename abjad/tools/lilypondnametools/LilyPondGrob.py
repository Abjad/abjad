# -*- coding: utf-8 -*-
from abjad.tools import abctools


class LilyPondGrob(abctools.AbjadValueObject):
    r'''A LilyPond grob.

    ::

        >>> grob = lilypondnametools.LilyPondGrob('Beam')
        >>> print(format(grob))
        lilypondnametools.LilyPondGrob(
            name='Beam',
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        )

    _identity_map = {}

    ### CONSTRUCTOR ###

    def __new__(class_, name='NoteHead'):
        if name in class_._identity_map:
            obj = class_._identity_map[name]
        else:
            obj = object.__new__(class_)
            class_._identity_map[name] = obj
        return obj

    ### INITIALIZER ###

    def __init__(self, name='NoteHead'):
        from abjad.ly import grob_interfaces
        assert name in grob_interfaces
        self._name = name

    ### PUBLIC METHODS ###

    @staticmethod
    def list_all_grobs():
        r'''Lists all grobs.

        ::

            >>> for lilypond_grob in lilypondnametools.LilyPondGrob.list_all_grobs():
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
            LilyPondGrob(name='VerticalAlignment')
            LilyPondGrob(name='VerticalAxisGroup')
            LilyPondGrob(name='VoiceFollower')
            LilyPondGrob(name='VoltaBracket')
            LilyPondGrob(name='VoltaBracketSpanner')

        Returns tuple.
        '''
        from abjad.ly import grob_interfaces
        return tuple(LilyPondGrob(name) for name in sorted(grob_interfaces))

    ### PUBLIC PROPERTIES ###

    @property
    def interfaces(self):
        r'''Gets interfaces of LilyPond grob.

        ::

            >>> for interface in grob.interfaces:
            ...     interface
            ...
            LilyPondGrobInterface(name='beam-interface')
            LilyPondGrobInterface(name='font-interface')
            LilyPondGrobInterface(name='grob-interface')
            LilyPondGrobInterface(name='spanner-interface')
            LilyPondGrobInterface(name='staff-symbol-referencer-interface')
            LilyPondGrobInterface(name='unbreakable-spanner-interface')

        Returns tuple.
        '''
        from abjad.ly import grob_interfaces
        from abjad.tools import lilypondnametools
        return tuple(
            lilypondnametools.LilyPondGrobInterface(_)
            for _ in sorted(grob_interfaces[self.name])
            )

    @property
    def name(self):
        r'''Gets name of LilyPond grob.

        ::

            >>> grob.name
            'Beam'

        Returns string.
        '''
        return self._name

    @property
    def property_names(self):
        r'''Gets property names of LilyPond grob.

        ::

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
            'whiteout-box'

        Returns tuple.
        '''
        property_names = set()
        for interface in self.interfaces:
            property_names.update(interface.property_names)
        return tuple(sorted(property_names))
