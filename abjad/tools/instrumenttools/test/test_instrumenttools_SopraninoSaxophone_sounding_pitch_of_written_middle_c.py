# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_SopraninoSaxophone_sounding_pitch_of_written_middle_c_01():

    sopranino_saxophone = instrumenttools.SopraninoSaxophone()

    assert sopranino_saxophone.sounding_pitch_of_written_middle_c == "ef'"
