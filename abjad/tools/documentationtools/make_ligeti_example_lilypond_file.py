# -*- encoding: utf-8 -*-
from abjad.tools import lilypondfiletools
from abjad.tools import schemetools
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import set_


def make_ligeti_example_lilypond_file(music=None):
    r'''Make Ligeti example LilyPond file.

    Returns LilyPond file.
    '''

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
    override(context_block).beam.breakable = True
    override(context_block).glissando.breakable = True
    override(context_block).note_column.ignore_collision = True
    override(context_block).spacing_spanner.uniform_stretching = True
    override(context_block).text_script.staff_padding = 4
    override(context_block).text_spanner.breakable = True
    override(context_block).tuplet_bracket.bracket_visibility = True
    override(context_block).tuplet_bracket.minimum_length = 3
    override(context_block).tuplet_bracket.padding = 2
    override(context_block).tuplet_bracket.springs_and_rods = \
        schemetools.Scheme('ly:spanner::set-spacing-rods')
    override(context_block).tuplet_number.text = \
        schemetools.Scheme('tuplet-number::calc-fraction-text')
    set_(context_block).autoBeaming = False
    moment = schemetools.SchemeMoment((1, 12))
    set_(context_block).proportionalNotationDuration = moment
    set_(context_block).tupletFullLength = True

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Staff'
    # LilyPond CAUTION: Timing_translator must appear 
    #                   before Default_bar_line_engraver!
    context_block.engraver_consists.append('Timing_translator')
    context_block.engraver_consists.append('Default_bar_line_engraver')
    override(context_block).time_signature.style = \
        schemetools.Scheme("'numbered")

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'RhythmicStaff'
    # LilyPond CAUTION: Timing_translator must appear 
    #                   before Default_bar_line_engraver!
    context_block.engraver_consists.append('Timing_translator')
    context_block.engraver_consists.append('Default_bar_line_engraver')
    override(context_block).time_signature.style = \
        schemetools.Scheme("'numbered")
    override(context_block).vertical_axis_group.minimum_Y_extent = (-2, 4)

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Voice'
    context_block.engraver_removals.append('Forbid_line_break_engraver')

    return lilypond_file
