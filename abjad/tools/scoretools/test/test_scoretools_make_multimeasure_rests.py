# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_multimeasure_rests_01():

    mmrs = scoretools.make_multimeasure_rests([(4, 8), (6, 8), (7, 8)])
    staff = Staff(mmrs)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            R2
            R2.
            R2..
        }
        '''
        )

    format(staff) == '\\new Staff {\n\tR2\n\tR2.\n\tR2..\n}'
