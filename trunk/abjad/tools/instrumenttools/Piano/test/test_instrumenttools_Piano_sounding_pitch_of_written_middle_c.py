# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Piano_sounding_pitch_of_written_middle_c_01():

    piano = instrumenttools.Piano()

    assert piano.sounding_pitch_of_written_middle_c == "c'"
