# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_LayoutBlock_lilypond_command_01():

    staff = Staff("fs'2 fs'2 gs'2 gs'2")
    score = Score([staff])
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    lilypond_file.layout_block.append(indicatortools.LilyPondCommand('accidentalStyle forget'))

    assert systemtools.TestManager.compare(
        lilypond_file.layout_block,
        r'''
        \layout {
            \accidentalStyle forget
        }
        '''
        )
