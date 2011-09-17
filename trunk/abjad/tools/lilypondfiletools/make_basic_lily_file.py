from abjad.tools.lilypondfiletools.HeaderBlock import HeaderBlock
from abjad.tools.lilypondfiletools.LayoutBlock import LayoutBlock
from abjad.tools.lilypondfiletools.LilyFile import LilyFile
from abjad.tools.lilypondfiletools.PaperBlock import PaperBlock
from abjad.tools.lilypondfiletools.ScoreBlock import ScoreBlock


def make_basic_lily_file(music = None):
    r'''.. versionadded:: 2.0

    Make basic LilyPond file with `music`::

        abjad> score = Score([Staff("c'8 d'8 e'8 f'8")])
        abjad> lily_file = lilypondfiletools.make_basic_lily_file(score)
        abjad> lily_file.header_block.composer = markuptools.Markup('Josquin')
        abjad> lily_file.layout_block.indent = 0
        abjad> lily_file.paper_block.top_margin = 15
        abjad> lily_file.paper_block.left_margin = 15

    ::

        abjad> f(lily_file) # doctest: +SKIP
        \header {
            composer = \markup { Josquin }
        }

        \layout {
            indent = #0
        }

        \paper {
            left-margin = #15
            top-margin = #15
        }

        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>

    Equip LilyPond file with header, layout and paper blocks.

    Return LilyPond file.
    '''

    lily_file = LilyFile()

    header_block = HeaderBlock()
    layout_block = LayoutBlock()
    paper_block = PaperBlock()
    score_block = ScoreBlock()

    lily_file.extend([header_block, layout_block, paper_block, score_block])

    lily_file.header_block = header_block
    lily_file.layout_block = layout_block
    lily_file.paper_block = paper_block
    lily_file.score_block = score_block

    if music is not None:
        score_block.append(music)
        music.lily_file = lily_file

    return lily_file
