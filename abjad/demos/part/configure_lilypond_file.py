# -*- coding: utf-8 -*-
import abjad


def configure_lilypond_file(lilypond_file):
    r'''Configures LilyPond file.
    '''

    lilypond_file._global_staff_size = 8

    context_block = abjad.ContextBlock(
        source_context_name=r'Staff \RemoveEmptyStaves',
        )
    abjad.override(context_block).vertical_axis_group.remove_first = True
    lilypond_file.layout_block.items.append(context_block)

    slash_separator = abjad.LilyPondCommand('slashSeparator')
    lilypond_file.paper_block.system_separator_markup = slash_separator

    bottom_margin = abjad.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.bottom_margin = bottom_margin

    top_margin = abjad.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.top_margin = top_margin

    left_margin = abjad.LilyPondDimension(0.75, 'in')
    lilypond_file.paper_block.left_margin = left_margin

    right_margin = abjad.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.right_margin = right_margin

    paper_width = abjad.LilyPondDimension(5.25, 'in')
    lilypond_file.paper_block.paper_width = paper_width

    paper_height = abjad.LilyPondDimension(7.25, 'in')
    lilypond_file.paper_block.paper_height = paper_height

    lilypond_file.header_block.composer = abjad.Markup('Arvo Pärt')
    title = 'Cantus in Memory of Benjamin Britten (1980)'
    lilypond_file.header_block.title = abjad.Markup(title)
