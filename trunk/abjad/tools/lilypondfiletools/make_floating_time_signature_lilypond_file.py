from abjad.tools import schemetools


def make_floating_time_signature_lilypond_file(music=None):
    r'''.. versionadded:: 2.10

    Make floating time signature LilyPond file from `music`.

    Function creates a basic LilyPond file.

    Function then applies many layout settings.

    View source here for the complete inventory of settings applied.

    Returns LilyPond file object.
    '''
    # TODO: lilypondfiletools should depend on layouttools and NOT the other way around
    from abjad.tools import layouttools
    from abjad.tools import lilypondfiletools

    lilypond_file = lilypondfiletools.make_basic_lilypond_file(music=music)

    lilypond_file.default_paper_size = 'letter', 'portrait'
    lilypond_file.global_staff_size = 12

    lilypond_file.paper_block.left_margin = 20
    lilypond_file.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)

    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True

    time_signature_context_block = lilypondfiletools.make_time_signature_context_block(font_size=1, padding=6)
    lilypond_file.layout_block.context_blocks.append(time_signature_context_block)

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    lilypond_file.score = context_block
    context_block.context_name = 'Score'
    context_block.accepts.append('TimeSignatureContext')
    context_block.engraver_removals.append('Bar_number_engraver')
    context_block.override.beam.breakable = True
    context_block.override.spacing_spanner.strict_grace_spacing = True
    context_block.override.spacing_spanner.strict_note_spacing = True
    context_block.override.spacing_spanner.uniform_stretching = True
    context_block.override.tuplet_bracket.bracket_visibility = True
    context_block.override.tuplet_bracket.padding = 2
    context_block.override.tuplet_bracket.springs_and_rods = schemetools.Scheme(
        'ly:spanner::set-spacing-rods')
    context_block.override.tuplet_bracket.minimum_length = 3
    context_block.override.tuplet_number.text = schemetools.Scheme('tuplet-number::calc-fraction-text')
    context_block.set.autoBeaming = False
    context_block.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 32))
    context_block.set.tupletFullLength = True

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Staff'
    context_block.engraver_removals.append('Time_signature_engraver')

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'RhythmicStaff'
    context_block.engraver_removals.append('Time_signature_engraver')

    return lilypond_file
