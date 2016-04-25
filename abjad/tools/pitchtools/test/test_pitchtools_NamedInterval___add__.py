# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval___add___01():

    mdi1 = pitchtools.NamedInterval('major', 2)
    mdi2 = pitchtools.NamedInterval('major', 3)
    new = mdi1 + mdi2

    assert new == pitchtools.NamedInterval('augmented', 4)
