# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval___mul___01():

    major_second = pitchtools.NamedMelodicInterval('major', 2)

    assert major_second * 0 == pitchtools.NamedMelodicInterval('perfect', 1)
    assert major_second * 1 == pitchtools.NamedMelodicInterval('major', 2)
    assert major_second * 2 == pitchtools.NamedMelodicInterval('major', 3)
    assert major_second * 3 == pitchtools.NamedMelodicInterval('augmented', 4)


def test_NamedMelodicInterval___mul___02():
    r'''Negative multiplicands work correctly.
    '''

    ascending_major_second = pitchtools.NamedMelodicInterval('+m2')
    descending_major_second = pitchtools.NamedMelodicInterval('-m2')

    assert ascending_major_second * -1 == descending_major_second
    assert descending_major_second * -1 == ascending_major_second
