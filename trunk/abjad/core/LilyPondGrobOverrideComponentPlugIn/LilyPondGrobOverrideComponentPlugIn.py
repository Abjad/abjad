from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy
from abjad.core.LilyPondGrobProxyContextWrapper import LilyPondGrobProxyContextWrapper
from abjad.core._LilyPondComponentPlugIn import _LilyPondComponentPlugIn


class LilyPondGrobOverrideComponentPlugIn(_LilyPondComponentPlugIn):
    '''.. versionadded:: 2.0

    LilyPond grob override component plug-in.
    '''

    _known_lilypond_context_names = set([
        'choir_staff', 'chord_names', 'cue_voice', 'devnull', 'drum_staff',
        'drum_voice', 'dynamics', 'figured_bass', 'fret_boards', 'global',
        'grand_staff', 'gregorian_transcription_staff', 'gregorian_transcription_voice',
        'lyrics', 'mensural_staff', 'mensural_voice', 'note_names', 'piano_staff',
        'rhythmic_staff', 'score', 'staff', 'staff_group', 'tab_staff',
        'tab_voice', 'vaticana_staff', 'vaticana_voice', 'voice'])

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
        'harmonic_parentheses_item', 'horizontal_bracket', 'instrument_name', 'instrument_switch',
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
        if name.startswith('_'):
            try:
                return vars(self)[name]
            except KeyError:
                raise AttributeError('"%s" object has no attribute: "%s".' % (
                    self.__class__.__name__, name))
        elif name in type(self)._known_lilypond_context_names:
            try:
                return vars(self)['_' + name]
            except KeyError:
                context = LilyPondGrobProxyContextWrapper()
                vars(self)['_' + name] = context
                return context
        elif name in type(self)._known_lilypond_grob_names:
            try:
                return vars(self)[name]
            except KeyError:
                vars(self)[name] = LilyPondGrobProxy()
                return vars(self)[name]
        else:
            return vars(self)[name]

    def __repr__(self):
        body_string = ' '
        skeleton_strings = self._get_skeleton_strings()
        if skeleton_strings:
            # remove 'override__'
            skeleton_strings = [x[10:] for x in skeleton_strings]
            skeleton_strings.sort()
            body_string = ', '.join(skeleton_strings)
        return '%s(%s)' % (self.__class__.__name__, body_string)

    def __setattr__(self, attr, value):
        # make sure attr is valid grob name before setting value #
        attr_value = getattr(self, attr)
        object.__setattr__(self, attr, value)

    ### PRIVATE ATTRIBUTES ###

    def _get_attribute_tuples(self):
        result = []
        for name, value in vars(self).iteritems():
            if isinstance(value, LilyPondGrobProxy):
                grob_name, grob_proxy = name, value
                for attribute_name, attribute_value in vars(grob_proxy).iteritems():
                    result.append((grob_name, attribute_name, attribute_value))
            else:
                context_name, context_proxy = name.strip('_'), value
                for grob_name, grob_proxy in vars(context_proxy).iteritems():
                    for attribute_name, attribute_value in vars(grob_proxy).iteritems():
                        result.append((context_name, grob_name, attribute_name, attribute_value))
        return tuple(result)

    def _get_skeleton_strings(self):
        skeleton_strings = []
        grob_override_tuples = self._get_attribute_tuples()
        for grob_override_tuple in grob_override_tuples:
            most = '__'.join(grob_override_tuple[:-1])
            value = grob_override_tuple[-1]
            skeleton_string = 'override__%s = %s' % (most, repr(value))
            skeleton_strings.append(skeleton_string)
        return tuple(skeleton_strings)

    ### PRIVATE METHODS ###

    def _list_format_contributions(self, contribution_type, is_once = False):
        from abjad.tools.lilypondfiletools._make_lilypond_override_string import _make_lilypond_override_string
        from abjad.tools.lilypondfiletools._make_lilypond_revert_string import _make_lilypond_revert_string
        assert contribution_type in ('override', 'revert')
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 3:
                context_name = None
                grob_name, attribute_name, attribute_value = attribute_tuple
            elif len(attribute_tuple) == 4:
                context_name, grob_name, attribute_name, attribute_value = attribute_tuple
            else:
                raise ValueError
            if contribution_type == 'override':
                result.append(_make_lilypond_override_string(grob_name, attribute_name,
                    attribute_value, context_name = context_name, is_once = is_once))
            else:
                result.append(
                    _make_lilypond_revert_string(grob_name, attribute_name, context_name = context_name))
        result.sort()
        return result
