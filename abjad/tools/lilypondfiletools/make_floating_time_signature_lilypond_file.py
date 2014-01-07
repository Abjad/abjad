# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import schemetools
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import set_


def make_floating_time_signature_lilypond_file(music=None):
    r'''Make floating time signature LilyPond file from `music`.

    Function creates a basic LilyPond file.

    Function then applies many layout settings.

    View source here for the complete inventory of settings applied.

    Returns LilyPond file object.
    '''
    from abjad.tools import layouttools
    from abjad.tools import lilypondfiletools

    lilypond_file = lilypondfiletools.make_basic_lilypond_file(music=music)

    lilypond_file.default_paper_size = 'letter', 'portrait'
    lilypond_file.global_staff_size = 12

    lilypond_file.paper_block.left_margin = 20
    vector = layouttools.make_spacing_vector(0, 0, 12, 0)
    lilypond_file.paper_block.system_system_spacing = vector

    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    command = indicatortools.LilyPondCommand('accidentalStyle forget')
    lilypond_file.layout_block.items.append(command)

    time_signature_context_block = \
        lilypondfiletools.make_time_signature_context_block(
        font_size=1, padding=6)
    lilypond_file.layout_block.context_blocks.append(
        time_signature_context_block)

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    lilypond_file.score = context_block
    context_block.context_name = 'Score'
    context_block.accepts_commands.append('TimeSignatureContext')
    context_block.remove_commands.append('Bar_number_engraver')
    override(context_block).beam.breakable = True
    override(context_block).spacing_spanner.strict_grace_spacing = True
    override(context_block).spacing_spanner.strict_note_spacing = True
    override(context_block).spacing_spanner.uniform_stretching = True
    override(context_block).tuplet_bracket.bracket_visibility = True
    override(context_block).tuplet_bracket.padding = 2
    scheme = schemetools.Scheme('ly:spanner::set-spacing-rods')
    override(context_block).tuplet_bracket.springs_and_rods = scheme
    override(context_block).tuplet_bracket.minimum_length = 3
    scheme = schemetools.Scheme('tuplet-number::calc-fraction-text')
    override(context_block).tuplet_number.text = scheme
    set_(context_block).autoBeaming = False
    moment = schemetools.SchemeMoment((1, 32))
    set_(context_block).proportionalNotationDuration = moment
    set_(context_block).tupletFullLength = True

    # provided as a stub position for user customization
    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'StaffGroup'

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Staff'
    context_block.remove_commands.append('Time_signature_engraver')

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'RhythmicStaff'
    context_block.remove_commands.append('Time_signature_engraver')

    return lilypond_file
