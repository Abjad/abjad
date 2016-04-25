# -*- coding: utf-8 -*-
from abjad.tools import lilypondfiletools
from abjad.tools import schemetools
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import set_


def make_ligeti_example_lilypond_file(music=None):
    r'''Makes Ligeti example LilyPond file.

    Returns LilyPond file.
    '''

    lilypond_file = lilypondfiletools.make_basic_lilypond_file(
        music=music,
        default_paper_size=('a4', 'letter'),
        global_staff_size=14,
        )

    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.layout_block.merge_differently_dotted = True
    lilypond_file.layout_block.merge_differently_headed = True

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Score',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.remove_commands.append('Bar_number_engraver')
    context_block.remove_commands.append('Default_bar_line_engraver')
    context_block.remove_commands.append('Timing_translator')
    override(context_block).beam.breakable = True
    override(context_block).glissando.breakable = True
    override(context_block).note_column.ignore_collision = True
    override(context_block).spacing_spanner.uniform_stretching = True
    override(context_block).text_script.staff_padding = 4
    override(context_block).text_spanner.breakable = True
    override(context_block).tuplet_bracket.bracket_visibility = True
    override(context_block).tuplet_bracket.minimum_length = 3
    override(context_block).tuplet_bracket.padding = 2
    scheme = schemetools.Scheme('ly:spanner::set-spacing-rods')
    override(context_block).tuplet_bracket.springs_and_rods = scheme
    scheme = schemetools.Scheme('tuplet-number::calc-fraction-text')
    override(context_block).tuplet_number.text = scheme
    set_(context_block).autoBeaming = False
    moment = schemetools.SchemeMoment((1, 12))
    set_(context_block).proportionalNotationDuration = moment
    set_(context_block).tupletFullLength = True

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Staff',
        )
    lilypond_file.layout_block.items.append(context_block)
    # LilyPond CAUTION: Timing_translator must appear
    #                   before Default_bar_line_engraver!
    context_block.consists_commands.append('Timing_translator')
    context_block.consists_commands.append('Default_bar_line_engraver')
    scheme = schemetools.Scheme("'numbered")
    override(context_block).time_signature.style = scheme

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='RhythmicStaff',
        )
    lilypond_file.layout_block.items.append(context_block)
    # LilyPond CAUTION: Timing_translator must appear
    #                   before Default_bar_line_engraver!
    context_block.consists_commands.append('Timing_translator')
    context_block.consists_commands.append('Default_bar_line_engraver')
    scheme = schemetools.Scheme("'numbered")
    override(context_block).time_signature.style = scheme
    override(context_block).vertical_axis_group.minimum_Y_extent = (-2, 4)

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Voice',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.remove_commands.append('Forbid_line_break_engraver')

    return lilypond_file
