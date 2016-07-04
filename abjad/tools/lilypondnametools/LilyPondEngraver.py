# -*- coding: utf-8 -*-
from abjad.tools import abctools


class LilyPondEngraver(abctools.AbjadValueObject):
    r'''A LilyPond engraver.

    ::

        >>> engraver = lilypondnametools.LilyPondEngraver('Auto_beam_engraver')
        >>> print(format(engraver))
        lilypondnametools.LilyPondEngraver(
            name='Auto_beam_engraver',
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        )

    _identity_map = {}

    ### CONSTRUCTOR ###

    def __new__(class_, name='Note_heads_engraver'):
        if name in class_._identity_map:
            obj = class_._identity_map[name]
        else:
            obj = object.__new__(class_)
            class_._identity_map[name] = obj
        return obj

    ### INITIALIZER ###

    def __init__(self, name='Note_heads_engraver'):
        from abjad.ly import engravers
        assert name in engravers
        self._name = name

    ### PUBLIC METHODS ###

    @staticmethod
    def list_all_engravers():
        r'''Lists all engravers.

        ::

            >>> for lilypond_engraver in lilypondnametools.LilyPondEngraver.list_all_engravers():
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
            LilyPondEngraver(name='Engraver')
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
            LilyPondEngraver(name='Measure_grouping_engraver')
            LilyPondEngraver(name='Melody_engraver')
            LilyPondEngraver(name='Mensural_ligature_engraver')
            LilyPondEngraver(name='Metronome_mark_engraver')
            LilyPondEngraver(name='Midi_control_function_performer')
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
            LilyPondEngraver(name='Scheme_engraver')
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
            LilyPondEngraver(name='Translator')
            LilyPondEngraver(name='Trill_spanner_engraver')
            LilyPondEngraver(name='Tuplet_engraver')
            LilyPondEngraver(name='Tweak_engraver')
            LilyPondEngraver(name='Vaticana_ligature_engraver')
            LilyPondEngraver(name='Vertical_align_engraver')
            LilyPondEngraver(name='Volta_engraver')

        Returns tuple.
        '''
        from abjad.ly import engravers
        return tuple(LilyPondEngraver(name=name) for name in sorted(engravers))

    ### PUBLIC PROPERTIES ###

    @property
    def grobs(self):
        r'''Gets LilyPond engraver's created grobs.

        ::

            >>> for grob in engraver.grobs:
            ...     grob
            ...
            LilyPondGrob(name='Beam')

        Returns tuple.
        '''
        from abjad.ly import engravers
        from abjad.tools import lilypondnametools
        return tuple(
            lilypondnametools.LilyPondGrob(name=name)
            for name in engravers[self.name]['grobs_created']
            )

    @property
    def name(self):
        r'''Gets name of LilyPond engraver.

        ::

            >>> engraver.name
            'Auto_beam_engraver'

        Returns string.
        '''
        return self._name

    @property
    def property_names(self):
        r'''Gets LilyPond engraver's property names.

        ::

            >>> for property_name in engraver.property_names:
            ...     property_name
            ...
            'autoBeaming'
            'baseMoment'
            'beamExceptions'
            'beamHalfMeasure'
            'beatStructure'
            'subdivideBeams'

        '''
        from abjad.ly import engravers
        property_names = set()
        property_names.update(engravers[self.name]['properties_read'])
        property_names.update(engravers[self.name]['properties_written'])
        return tuple(sorted(property_names))
