# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval___add___01():

    mdi1 = pitchtools.NamedMelodicInterval('major', 2)
    mdi2 = pitchtools.NamedMelodicInterval('major', 3)
    new = mdi1 + mdi2

    assert new == pitchtools.NamedMelodicInterval('augmented', 4)
