# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Viola_sounding_pitch_of_written_middle_c_01():

    viola = instrumenttools.Viola()

    assert viola.sounding_pitch_of_written_middle_c == "c'"
