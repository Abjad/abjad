# -*- encoding: utf-8 -*-
from abjad import *


def format_lilypond_file(score):

    spacing_vector = layouttools.make_spacing_vector(0, 0, 8, 0)
    score.override.vertical_axis_group.staff_staff_spacing = spacing_vector
    score.override.staff_grouper.staff_staff_spacing = spacing_vector
    score.set.mark_formatter = schemetools.Scheme('format-mark-box-numbers')

    #score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 8)
    #score.override.spacing_spanner.uniform_stretching = False
    #score.override.spacing_spanner.strict_note_spacing = False

    #score.override.system_start_bar.thickness = 15
    #score.override.system_start_square.padding = 3
    #score.override.system_start_square.thickness = 5
    #score.override.system_start_bracket.padding = 2.5
    #score.override.rehearsal_mark.padding = 1.3
    #score.override.rehearsal_mark.font_name = "Futura"
    #score.override.script.padding = 0.9

    lily = lilypondfiletools.make_basic_lilypond_file(score)
    lily.global_staff_size = 8

    context_block = lilypondfiletools.ContextBlock()
    context_block.context_name = r'Staff \RemoveEmptyStaves'
    context_block.override.vertical_axis_group.remove_first = True
    lily.layout_block.context_blocks.append(context_block)

    lily.paper_block.system_separator_markup = marktools.LilyPondCommandMark('slashSeparator')
    lily.paper_block.bottom_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
    lily.paper_block.top_margin =    lilypondfiletools.LilyPondDimension(0.5, 'in')
    lily.paper_block.left_margin =   lilypondfiletools.LilyPondDimension(0.75, 'in')
    lily.paper_block.right_margin =  lilypondfiletools.LilyPondDimension(0.5, 'in')
    lily.paper_block.paper_width =   lilypondfiletools.LilyPondDimension(5.25, 'in')
    lily.paper_block.paper_height =  lilypondfiletools.LilyPondDimension(7.25, 'in')

    lily.header_block.composer = markuptools.Markup('Arvo Pärt')
    lily.header_block.title = markuptools.Markup('Cantus in Memory of Benjamin Britten (1980)')

    return lily

