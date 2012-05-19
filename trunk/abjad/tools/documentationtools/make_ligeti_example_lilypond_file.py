def make_ligeti_example_lilypond_file(music=None):
    r'''.. versionadded:: 2.9

    Make Ligeti example LilyPond file.

    Return LilyPond file.
    '''
    from abjad.tools import lilypondfiletools
    from abjad.tools import schemetools

    lilypond_file = lilypondfiletools.make_basic_lilypond_file(music=music)

    lilypond_file.default_paper_size = 'a4', 'letter'
    lilypond_file.global_staff_size = 14

    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.layout_block.merge_differently_dotted = True
    lilypond_file.layout_block.merge_differently_headed = True

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Score'
    context_block.engraver_removals.append('Bar_number_engraver')
    context_block.engraver_removals.append('Default_bar_line_engraver')
    context_block.engraver_removals.append('Timing_translator')
    context_block.override.beam.breakable = True
    context_block.override.glissando.breakable = True
    context_block.override.note_column.ignore_collision = True
    #context_block.override.spacing_spanner.strict_grace_spacing = True
    #context_block.override.spacing_spanner.strict_note_spacing = True
    context_block.override.spacing_spanner.uniform_stretching = True
    context_block.override.text_script.staff_padding = 4
    context_block.override.text_spanner.breakable = True
    context_block.override.tuplet_bracket.bracket_visibility = True
    context_block.override.tuplet_bracket.minimum_length = 3
    context_block.override.tuplet_bracket.padding = 2
    context_block.override.tuplet_bracket.springs_and_rods = schemetools.Scheme(
        'ly:spanner::set-spacing-rods')
    context_block.override.tuplet_number.text = schemetools.Scheme('tuplet-number::calc-fraction-text')
    context_block.set.autoBeaming = False
    context_block.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 12))
    context_block.set.tupletFullLength = True

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Staff'
    # LilyPond CAUTION: Timing_translator must appear before Default_bar_line_engraver!
    context_block.engraver_consists.append('Timing_translator') 
    context_block.engraver_consists.append('Default_bar_line_engraver') 
    context_block.override.time_signature.style = schemetools.Scheme("'numbered")

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'RhythmicStaff'
    # LilyPond CAUTION: Timing_translator must appear before Default_bar_line_engraver!
    context_block.engraver_consists.append('Timing_translator') 
    context_block.engraver_consists.append('Default_bar_line_engraver') 
    context_block.override.time_signature.style = schemetools.Scheme("'numbered")
    context_block.override.vertical_axis_group.minimum_Y_extent = (-2, 4)

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Voice'
    context_block.engraver_removals.append('Forbid_line_break_engraver')

    return lilypond_file
