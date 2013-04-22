# -*- encoding: utf-8 -*-
from abjad import *


def configure_lilypond_file(lilypond_file):

    lilypond_file.global_staff_size = 8

    context_block = lilypondfiletools.ContextBlock()
    context_block.context_name = r'Staff \RemoveEmptyStaves'
    context_block.override.vertical_axis_group.remove_first = True
    lilypond_file.layout_block.context_blocks.append(context_block)

    lilypond_file.paper_block.system_separator_markup = marktools.LilyPondCommandMark('slashSeparator')
    lilypond_file.paper_block.bottom_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.top_margin =    lilypondfiletools.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.left_margin =   lilypondfiletools.LilyPondDimension(0.75, 'in')
    lilypond_file.paper_block.right_margin =  lilypondfiletools.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.paper_width =   lilypondfiletools.LilyPondDimension(5.25, 'in')
    lilypond_file.paper_block.paper_height =  lilypondfiletools.LilyPondDimension(7.25, 'in')

    lilypond_file.header_block.composer = markuptools.Markup('Arvo Pärt')
    lilypond_file.header_block.title = markuptools.Markup('Cantus in Memory of Benjamin Britten (1980)')
