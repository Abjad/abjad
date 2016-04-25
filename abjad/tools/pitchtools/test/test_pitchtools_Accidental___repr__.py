# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental___repr___01():

    accidental = pitchtools.Accidental('s')
    assert repr(accidental) == "Accidental('s')"
