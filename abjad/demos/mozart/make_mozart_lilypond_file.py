# -*- coding: utf-8 -*-
import abjad
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from abjad.tools import schemetools


def make_mozart_lilypond_file():
    r'''Makes Mozart LilyPond file.
    '''

    score = abjad.demos.mozart.make_mozart_score()
    lily = lilypondfiletools.make_basic_lilypond_file(
        music=score,
        global_staff_size=12,
        )
    title = markuptools.Markup(r'\bold \sans "Ein Musikalisches Wuerfelspiel"')
    composer = schemetools.Scheme("W. A. Mozart (maybe?)")
    lily.header_block.title = title
    lily.header_block.composer = composer
    lily.layout_block.ragged_right = True
    lily.paper_block.markup_system_spacing = schemetools.SchemeAssociativeList(
        ('basic_distance', 8),
        )
    lily.paper_block.paper_width = 180
    return lily
