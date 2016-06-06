# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Measure___format___01():

    measure = Measure((4, 16), "c'8 c'16 c'16")
    
    assert format(measure, 'storage') == stringtools.normalize(
        r'''
        scoretools.Measure(
            indicatortools.TimeSignature((4, 16)),
            "c'8 c'16 c'16"
            )
        '''
        )


def test_scoretools_Measure___format___02():

    measure = Measure((4, 16), "c'8 c'16 c'16", implicit_scaling=True)
    
    assert format(measure, 'storage') == stringtools.normalize(
        r'''
        scoretools.Measure(
            indicatortools.TimeSignature((4, 16)),
            "c'8 c'16 c'16",
            implicit_scaling=True,
            )
        '''
        )
