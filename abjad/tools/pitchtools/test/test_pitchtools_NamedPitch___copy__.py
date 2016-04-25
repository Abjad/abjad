# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_pitchtools_NamedPitch___copy___01():

    pitch = NamedPitch(13)
    new = copy.copy(pitch)

    assert new is not pitch
    assert new.accidental is not pitch.accidental
