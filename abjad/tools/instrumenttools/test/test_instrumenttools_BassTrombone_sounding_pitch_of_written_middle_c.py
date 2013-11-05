# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_BassTrombone_sounding_pitch_of_written_middle_c_01():

    trombone = instrumenttools.BassTrombone()

    assert trombone.sounding_pitch_of_written_middle_c == "c'"
