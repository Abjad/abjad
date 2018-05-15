import abjad


def make_desordre_lilypond_file(score):
    """
    Makes Désordre LilyPond file.
    """
    lilypond_file = abjad.LilyPondFile.new(
        music=score,
        default_paper_size=('a4', 'letter'),
        global_staff_size=14,
        )

    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.layout_block.merge_differently_dotted = True
    lilypond_file.layout_block.merge_differently_headed = True

    context_block = abjad.ContextBlock(
        source_lilypond_type='Score',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.remove_commands.append('Bar_number_engraver')
    context_block.remove_commands.append('Default_bar_line_engraver')
    context_block.remove_commands.append('Timing_translator')
    abjad.override(context_block).beam.breakable = True
    abjad.override(context_block).glissando.breakable = True
    abjad.override(context_block).note_column.ignore_collision = True
    abjad.override(context_block).spacing_spanner.uniform_stretching = True
    abjad.override(context_block).text_script.staff_padding = 4
    abjad.override(context_block).text_spanner.breakable = True
    abjad.override(context_block).tuplet_bracket.bracket_visibility = True
    abjad.override(context_block).tuplet_bracket.minimum_length = 3
    abjad.override(context_block).tuplet_bracket.padding = 2
    scheme = abjad.Scheme('ly:spanner::set-spacing-rods')
    abjad.override(context_block).tuplet_bracket.springs_and_rods = scheme
    scheme = abjad.Scheme('tuplet-number::calc-fraction-text')
    abjad.override(context_block).tuplet_number.text = scheme
    abjad.setting(context_block).autoBeaming = False
    moment = abjad.SchemeMoment((1, 12))
    abjad.setting(context_block).proportionalNotationDuration = moment
    abjad.setting(context_block).tupletFullLength = True

    context_block = abjad.ContextBlock(
        source_lilypond_type='Staff',
        )
    lilypond_file.layout_block.items.append(context_block)
    # LilyPond CAUTION: Timing_translator must appear
    #                   before Default_bar_line_engraver!
    context_block.consists_commands.append('Timing_translator')
    context_block.consists_commands.append('Default_bar_line_engraver')
    scheme = abjad.Scheme("'numbered")
    abjad.override(context_block).time_signature.style = scheme

    context_block = abjad.ContextBlock(
        source_lilypond_type='RhythmicStaff',
        )
    lilypond_file.layout_block.items.append(context_block)
    # LilyPond CAUTION: Timing_translator must appear
    #                   before Default_bar_line_engraver!
    context_block.consists_commands.append('Timing_translator')
    context_block.consists_commands.append('Default_bar_line_engraver')
    scheme = abjad.Scheme("'numbered")
    abjad.override(context_block).time_signature.style = scheme
    abjad.override(context_block).vertical_axis_group.minimum_Y_extent = (-2, 4)

    context_block = abjad.ContextBlock(
        source_lilypond_type='Voice',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.remove_commands.append('Forbid_line_break_engraver')

    return lilypond_file
