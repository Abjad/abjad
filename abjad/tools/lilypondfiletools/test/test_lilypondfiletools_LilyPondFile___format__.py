# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_LilyPondFile___format___01():

    staff = Staff("c'8 d'8 e'8 f'8")
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)
    lilypond_file.file_initial_system_comments[:] = []
    lilypond_file.file_initial_system_includes[:] = []
    lilypond_file.file_initial_user_comments.append('User comments 1.')
    lilypond_file.file_initial_user_comments.append('User comments 2.')
    lilypond_file.file_initial_user_includes.append('external-settings-file-1.ly')
    lilypond_file.file_initial_user_includes.append('external-settings-file-2.ly')
    lilypond_file.default_paper_size = 'letter', 'portrait'
    lilypond_file.global_staff_size = 16
    lilypond_file.header_block.composer = Markup('Josquin')
    lilypond_file.header_block.title = Markup('Missa sexti tonus')
    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.left_margin = 15
    lilypond_file.paper_block.oddFooterMarkup = Markup('The odd-page footer')
    lilypond_file.paper_block.evenFooterMarkup = Markup('The even-page footer')

    assert systemtools.TestManager.compare(
        lilypond_file,
        r'''
        % User comments 1.
        % User comments 2.

        \include "external-settings-file-1.ly"
        \include "external-settings-file-2.ly"

        #(set-default-paper-size "letter" 'portrait)
        #(set-global-staff-size 16)

        \header {
            composer = \markup { Josquin }
            title = \markup { Missa sexti tonus }
        }

        \layout {
            indent = #0
            left-margin = #15
        }

        \paper {
            evenFooterMarkup = \markup { The even-page footer }
            oddFooterMarkup = \markup { The odd-page footer }
        }

        \score {
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        }
        '''
        )


def test_lilypondfiletools_LilyPondFile___format___02():
    r'''With empty layout and MIDI blocks.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    score_block = lilypondfiletools.Block(name='score')
    layout_block = lilypondfiletools.LayoutBlock()
    midi_block = lilypondfiletools.Block(name='midi')

    score_block.items.append(score)
    score_block.items.append(layout_block)
    score_block.items.append(midi_block)

    assert systemtools.TestManager.compare(
        score_block,
        r'''
        \score {
            \new Score <<
                \new Staff {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>
            \layout {}
            \midi {}
        }
        '''
        )


def test_lilypondfiletools_LilyPondFile___format___03():
    r'''LilyPondFile implements default paper size and global 
    staff size attributes.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    lilypond_file = lilypondfiletools.LilyPondFile()
    lilypond_file.items.append(score)
    lilypond_file.default_paper_size = '11x17', 'landscape'
    lilypond_file.global_staff_size = 14
    lilypond_file.file_initial_system_comments[:] = []
    lilypond_file.file_initial_system_includes[:] = []

    assert systemtools.TestManager.compare(
        lilypond_file,
        r'''
        #(set-default-paper-size "11x17" 'landscape)
        #(set-global-staff-size 14)

        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        '''
        )
