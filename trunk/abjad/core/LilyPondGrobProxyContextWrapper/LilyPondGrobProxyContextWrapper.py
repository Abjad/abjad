from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy


class LilyPondGrobProxyContextWrapper(object):
    '''.. versionadded:: 2.0

    Context wrapper for LilyPond grob overrides.
    '''

    _known_lilypond_grob_names = set(['accidental', 'accidental_cautionary', 'accidental_placement',
        'accidental_suggestion', 'ambitus', 'ambitus_accidental', 'ambitus_line',
        'ambitus_note_head', 'arpeggio', 'balloon_text_item', 'bar_line', 'bar_number',
        'bass_figure', 'bass_figure_alignment', 'bass_figure_alignment_positioning',
        'bass_figure_bracket', 'bass_figure_continuation', 'bass_figure_line', 'beam',
        'bend_after', 'break_align_group', 'break_alignment', 'breathing_sign', 'chord_name',
        'clef', 'cluster_spanner', 'cluster_spanner_beacon', 'combine_text_script', 'custos',
        'dot_column', 'dots', 'double_percent_repeat', 'double_percent_repeat_counter',
        'dynamic_line_spanner', 'dynamic_text', 'dynamic_text_spanner', 'episema', 'fingering',
        'fret_board', 'glissando', 'grace_spacing', 'grid_line', 'grid_point', 'hairpin',
        'harmonic_parentheses_item', 'horizontal_bracket', 'instrument_name_markup', 'instrument_switch',
        'key_cancellation', 'key_signature', 'laissez_vibrer_tie', 'laissez_vibrer_tie_column',
        'ledger_line_spanner', 'left_edge', 'ligature_bracket', 'lyric_extender', 'lyric_hyphen',
        'lyric_space', 'lyric_text', 'measure_grouping', 'melody_item', 'mensural_ligature',
        'metronome_mark', 'multi_measure_rest', 'multi_measure_rest_number',
        'multi_measure_rest_text', 'non_musical_paper_column', 'note_collision', 'note_column',
        'note_head', 'note_name', 'note_spacing', 'octavate_eight', 'ottava_bracket',
        'paper_column', 'parentheses_item', 'percent_repeat', 'percent_repeat_counter',
        'phrasing_slur', 'piano_pedal_bracket', 'rehearsal_mark', 'repeat_slash', 'repeat_tie',
        'repeat_tie_column', 'rest', 'rest_collision', 'script', 'script_column', 'script_row',
        'slur', 'sostenuto_pedal', 'sostenuto_pedal_line_spanner', 'spacing_spanner', 'span_bar',
        'staff_grouper', 'staff_spacing', 'staff_symbol', 'stanza_number', 'stem', 'stem_tremolo',
        'string_number', 'stroke_finger', 'sustain_pedal', 'sustain_pedal_line_spanner', 'system',
        'system_start_bar', 'system_start_brace', 'system_start_bracket', 'system_start_square',
        'tab_note_head', 'text_script', 'text_spanner', 'tie', 'tie_column', 'time_signature',
        'trill_pitch_accidental', 'trill_pitch_group', 'trill_pitch_head', 'trill_spanner',
        'tuplet_bracket', 'tuplet_number', 'una_corda_pedal', 'una_corda_pedal_line_spanner',
        'vaticana_ligature', 'vertical_alignment', 'vertical_axis_group', 'voice_follower',
        'volta_bracket', 'volta_bracket_spanner'])

    ### OVERLOADS ###

    def __getattr__(self, name):
        try:
            return vars(self)[name]
        except KeyError:
            if name in type(self)._known_lilypond_grob_names:
                vars(self)[name] = LilyPondGrobProxy()
                return vars(self)[name]
            else:
                raise AttributeError('object can have only LilyPond grob attributes: "%s".' %
                    self.__class__.__name__)

    def __repr__(self):
        return '%s()' % self.__class__.__name__
