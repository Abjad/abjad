# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyFile_01():
    r'''LilyPondFile implements default paper size and global staff size attributes.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    lilypond_file = lilypondfiletools.LilyPondFile()
    lilypond_file.append(score)
    lilypond_file.default_paper_size = '11x17', 'landscape'
    lilypond_file.global_staff_size = 14
    lilypond_file.file_initial_system_comments = []
    lilypond_file.file_initial_system_includes = []

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

    assert testtools.compare(
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
