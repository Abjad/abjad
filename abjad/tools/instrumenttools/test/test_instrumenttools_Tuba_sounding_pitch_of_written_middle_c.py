# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Tuba_sounding_pitch_of_written_middle_c_01():

    tuba = instrumenttools.Tuba()

    assert tuba.sounding_pitch_of_written_middle_c == "c'"
