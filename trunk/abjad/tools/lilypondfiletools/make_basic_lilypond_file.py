def make_basic_lilypond_file(music=None):
    r'''.. versionadded:: 2.0

    Make basic LilyPond file with `music`::

        >>> score = Score([Staff("c'8 d'8 e'8 f'8")])
        >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        >>> lilypond_file.header_block.composer = markuptools.Markup('Josquin')
        >>> lilypond_file.layout_block.indent = 0
        >>> lilypond_file.paper_block.top_margin = 15
        >>> lilypond_file.paper_block.left_margin = 15

    ::

        >>> f(lilypond_file) # doctest: +SKIP
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
    from abjad.tools import lilypondfiletools

    lilypond_file = lilypondfiletools.LilyPondFile()

    header_block = lilypondfiletools.HeaderBlock()
    layout_block = lilypondfiletools.LayoutBlock()
    paper_block = lilypondfiletools.PaperBlock()
    score_block = lilypondfiletools.ScoreBlock()

    lilypond_file.extend([header_block, layout_block, paper_block, score_block])

    lilypond_file.header_block = header_block
    lilypond_file.layout_block = layout_block
    lilypond_file.paper_block = paper_block
    lilypond_file.score_block = score_block

    if music is not None:
        score_block.append(music)
        music.lilypond_file = lilypond_file

    return lilypond_file
