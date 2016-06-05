# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_Scale_make_notes_01():
    r'''Allow nonassignable durations.
    '''

    scale = tonalanalysistools.Scale('c', 'major')
    notes = scale.make_notes(2, Duration(5, 16))
    staff = Staff(notes)

    r'''
    \new Staff {
        c'4 ~
        c'16
        d'4 ~
        d'16
    }
    '''

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'4 ~
            c'16
            d'4 ~
            d'16
        }
        '''
        )
