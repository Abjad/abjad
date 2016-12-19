# -*- coding: utf-8 -*-
import abjad
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from abjad.tools import schemetools


def make_mozart_lilypond_file():
    r'''Makes Mozart LilyPond file.
    '''

    score = abjad.demos.mozart.make_mozart_score()
    lilypond_file = lilypondfiletools.LilyPondFile.new(
        music=score,
        global_staff_size=12,
        )
    title = markuptools.Markup(r'\bold \sans "Ein Musikalisches Wuerfelspiel"')
    composer = schemetools.Scheme("W. A. Mozart (maybe?)")
    lilypond_file.header_block.title = title
    lilypond_file.header_block.composer = composer
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.paper_block.markup_system_spacing = schemetools.SchemeAssociativeList(
        ('basic_distance', 8),
        )
    lilypond_file.paper_block.paper_width = 180
    return lilypond_file
