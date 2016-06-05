# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_MultimeasureRest___init___01():
    r'''Initializes multimeasure rest from empty input.
    '''

    multimeasure_rest = scoretools.MultimeasureRest()

    assert format(multimeasure_rest) == stringtools.normalize(
        r'''
        R4
        '''
        )

    assert inspect_(multimeasure_rest).is_well_formed()
