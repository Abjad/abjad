# -*- encoding: utf-8 -*-
from abjad.tools import scoretools


def make_basic_lilypond_file(music=None):
    r'''Makes basic LilyPond file with `music`.

    ::

        >>> score = Score([Staff("c'8 d'8 e'8 f'8")])
        >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        >>> lilypond_file.header_block.title = Markup('Missa sexti tonus')
        >>> lilypond_file.header_block.composer = Markup('Josquin')
        >>> lilypond_file.layout_block.indent = 0
        >>> lilypond_file.paper_block.top_margin = 15
        >>> lilypond_file.paper_block.left_margin = 15
        >>> show(lilypond_file) # doctest: +SKIP

    ..  doctest::

        >>> print format(lilypond_file) # doctest: +SKIP
        \header {
            composer = \markup { Josquin }
            title = \markup { Missa sexti tonus }
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

    Equips LilyPond file with header, layout and paper blocks.

    Returns LilyPond file.
    '''
    from abjad.tools import lilypondfiletools
    if isinstance(music, lilypondfiletools.LilyPondFile):
        return music
    lilypond_file = lilypondfiletools.LilyPondFile()
    header_block = lilypondfiletools.HeaderBlock()
    layout_block = lilypondfiletools.LayoutBlock()
    paper_block = lilypondfiletools.PaperBlock()
    score_block = lilypondfiletools.ScoreBlock()
    lilypond_file.items.extend([
        header_block,
        layout_block,
        paper_block,
        score_block,
        ])
    lilypond_file.header_block = header_block
    lilypond_file.layout_block = layout_block
    lilypond_file.paper_block = paper_block
    lilypond_file.score_block = score_block
    if music is not None:
        score_block.append(music)
    return lilypond_file
