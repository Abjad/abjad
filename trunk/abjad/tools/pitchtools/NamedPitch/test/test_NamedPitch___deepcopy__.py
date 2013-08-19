# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_NamedPitch___deepcopy___01():

    pitch = pitchtools.NamedPitch(13)
    new = copy.deepcopy(pitch)

    assert new is not pitch
    assert new._accidental is not pitch._accidental
