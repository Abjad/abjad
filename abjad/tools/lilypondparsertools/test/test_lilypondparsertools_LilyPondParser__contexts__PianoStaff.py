# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__contexts__PianoStaff_01():

    target = StaffGroup([
        Staff(scoretools.make_notes([0, 2, 4, 5, 7], (1, 8))),
        Staff(scoretools.make_notes([0, 2, 4, 5, 7], (1, 8)))
    ])
    target.context_name = 'PianoStaff'

    assert format(target) == stringtools.normalize(
        r'''
        \new PianoStaff <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
            \new Staff {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
