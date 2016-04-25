# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch___neg___01():

    assert -pitchtools.NumberedPitch(12) == -12
