# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_TenorSaxophone_sounding_pitch_of_written_middle_c_01():

    tenor_saxophone = instrumenttools.TenorSaxophone()

    assert tenor_saxophone.sounding_pitch_of_written_middle_c == 'bf,'
