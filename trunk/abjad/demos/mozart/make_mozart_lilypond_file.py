from abjad import *
from abjad.demos.mozart.make_mozart_score import make_mozart_score


def make_mozart_lilypond_file():
    score = make_mozart_score()
    lily = lilypondfiletools.make_basic_lilypond_file(score)
    title = markuptools.Markup(r'\bold \sans "Ein Musikalisches Wuerfelspiel"')
    composer = schemetools.Scheme("W. A. Mozart (maybe?)")
    lily.global_staff_size = 12
    lily.header_block.title = title
    lily.header_block.composer = composer
    lily.layout_block.ragged_right = True
    lily.paper_block.markup_system_spacing__basic_distance = 8
    lily.paper_block.paper_width = 180
    return lily
