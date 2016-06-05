# -*- coding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_make_basic_lily_file_01():

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(
        music=score,
        date_time_token=False,
        lilypond_language_token=False,
        lilypond_version_token=False,
        )
    lilypond_file.header_block.composer = Markup('Josquin')
    lilypond_file.layout_block.indent = 0
    lilypond_file.paper_block.top_margin = 15
    lilypond_file.paper_block.left_margin = 15

    assert lilypond_file.score_block.items[0] is score

    assert format(lilypond_file) == stringtools.normalize(
        r'''
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

        \score {
            \new Score <<
                \new Staff {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>
        }
        '''
        )
