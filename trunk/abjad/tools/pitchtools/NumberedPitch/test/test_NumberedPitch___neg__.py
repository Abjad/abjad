# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitch___neg___01():

    assert -pitchtools.NumberedPitch(12) == -12
