# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Harp_sounding_pitch_of_written_middle_c_01():

    harp = instrumenttools.Harp()

    assert harp.sounding_pitch_of_written_middle_c == "c'"
