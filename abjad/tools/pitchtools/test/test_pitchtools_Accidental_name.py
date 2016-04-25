# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental_name_01():

    assert pitchtools.Accidental('s').name == 'sharp'
    assert pitchtools.Accidental('f').name == 'flat'
