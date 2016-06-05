# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from abjad.tools.topleveltools import override


def configure_lilypond_file(lilypond_file):
    r'''Configures LilyPond file.
    '''

    lilypond_file._global_staff_size = 8

    context_block = lilypondfiletools.ContextBlock(
        source_context_name=r'Staff \RemoveEmptyStaves',
        )
    override(context_block).vertical_axis_group.remove_first = True
    lilypond_file.layout_block.items.append(context_block)

    slash_separator = indicatortools.LilyPondCommand('slashSeparator')
    lilypond_file.paper_block.system_separator_markup = slash_separator

    bottom_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.bottom_margin = bottom_margin

    top_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.top_margin = top_margin

    left_margin = lilypondfiletools.LilyPondDimension(0.75, 'in')
    lilypond_file.paper_block.left_margin = left_margin

    right_margin = lilypondfiletools.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.right_margin = right_margin

    paper_width = lilypondfiletools.LilyPondDimension(5.25, 'in')
    lilypond_file.paper_block.paper_width = paper_width

    paper_height = lilypondfiletools.LilyPondDimension(7.25, 'in')
    lilypond_file.paper_block.paper_height = paper_height

    lilypond_file.header_block.composer = markuptools.Markup('Arvo Pärt')
    title = 'Cantus in Memory of Benjamin Britten (1980)'
    lilypond_file.header_block.title = markuptools.Markup(title)