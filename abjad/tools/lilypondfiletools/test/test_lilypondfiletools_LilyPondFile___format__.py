# -*- coding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_LilyPondFile___format___01():
    r'''With empty layout and MIDI blocks.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    score_block = lilypondfiletools.Block(name='score')
    layout_block = lilypondfiletools.Block(name='layout')
    midi_block = lilypondfiletools.Block(name='midi')

    score_block.items.append(score)
    score_block.items.append(layout_block)
    score_block.items.append(midi_block)

    assert format(score_block) == stringtools.normalize(
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


def test_lilypondfiletools_LilyPondFile___format___02():
    r'''LilyPondFile implements default paper size and global
    staff size attributes.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    lilypond_file = lilypondfiletools.LilyPondFile(
        date_time_token=False,
        default_paper_size=('11x17', 'landscape'),
        global_staff_size=14,
        lilypond_language_token=False,
        lilypond_version_token=False,
        )
    lilypond_file.items.append(score)

    assert format(lilypond_file) == stringtools.normalize(
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
