# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval___mul___01():

    major_second = pitchtools.NamedInterval('major', 2)

    assert major_second * 0 == pitchtools.NamedInterval('perfect', 1)
    assert major_second * 1 == pitchtools.NamedInterval('major', 2)
    assert major_second * 2 == pitchtools.NamedInterval('major', 3)
    assert major_second * 3 == pitchtools.NamedInterval('augmented', 4)


def test_pitchtools_NamedInterval___mul___02():
    r'''Negative multiplicands work correctly.
    '''

    ascending_major_second = pitchtools.NamedInterval('+m2')
    descending_major_second = pitchtools.NamedInterval('-m2')

    assert ascending_major_second * -1 == descending_major_second
    assert descending_major_second * -1 == ascending_major_second
