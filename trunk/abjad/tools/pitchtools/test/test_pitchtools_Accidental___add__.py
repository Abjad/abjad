# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental___add___01():

    m = pitchtools.Accidental('quarter sharp')

    assert m + m == pitchtools.Accidental('sharp')
    assert m + m + m == pitchtools.Accidental('three-quarters sharp')
