from abjad.tools.lilypondfiletools.HeaderBlock import HeaderBlock
from abjad.tools.lilypondfiletools.LayoutBlock import LayoutBlock
from abjad.tools.lilypondfiletools.LilyPondFile import LilyPondFile
from abjad.tools.lilypondfiletools.PaperBlock import PaperBlock
from abjad.tools.lilypondfiletools.ScoreBlock import ScoreBlock


def make_basic_lilypond_file(music = None):
    r'''.. versionadded:: 2.0

    Make basic LilyPond file with `music`::

        abjad> score = Score([Staff("c'8 d'8 e'8 f'8")])
        abjad> lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        abjad> lilypond_file.header_block.composer = markuptools.Markup('Josquin')
        abjad> lilypond_file.layout_block.indent = 0
        abjad> lilypond_file.paper_block.top_margin = 15
        abjad> lilypond_file.paper_block.left_margin = 15

    ::

        abjad> f(lilypond_file) # doctest: +SKIP
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

    lilypond_file = LilyPondFile()

    header_block = HeaderBlock()
    layout_block = LayoutBlock()
    paper_block = PaperBlock()
    score_block = ScoreBlock()

    lilypond_file.extend([header_block, layout_block, paper_block, score_block])

    lilypond_file.header_block = header_block
    lilypond_file.layout_block = layout_block
    lilypond_file.paper_block = paper_block
    lilypond_file.score_block = score_block

    if music is not None:
        score_block.append(music)
        music.lilypond_file = lilypond_file

    return lilypond_file
