# -*- coding: utf-8 -*-
import abjad


def test_lilypondfiletools_LilyPondFile_new_01():

    score = abjad.Score([abjad.Staff("c'8 d'8 e'8 f'8")])
    lilypond_file = abjad.LilyPondFile.new(
        music=score,
        date_time_token=False,
        lilypond_language_token=False,
        lilypond_version_token=False,
        )
    lilypond_file.header_block.composer = abjad.Markup('Josquin')
    lilypond_file.layout_block.indent = 0
    lilypond_file.paper_block.top_margin = 15
    lilypond_file.paper_block.left_margin = 15

    assert lilypond_file[abjad.Score] is score

    assert format(lilypond_file) == abjad.String.normalize(
        r'''
        \header {
            composer = \markup { Josquin }
        }

        \layout {
            indent = #0
        }

        \paper {
            top-margin = #15
            left-margin = #15
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
