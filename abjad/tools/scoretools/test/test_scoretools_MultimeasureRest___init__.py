# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_MultimeasureRest___init___01():
    r'''Initializes multimeasure rest from empty input.
    '''
    
    multimeasure_rest = scoretools.MultimeasureRest()

    assert systemtools.TestManager.compare(
        multimeasure_rest,
        r'''
        R4
        '''
        )

    assert inspect(multimeasure_rest).is_well_formed()
