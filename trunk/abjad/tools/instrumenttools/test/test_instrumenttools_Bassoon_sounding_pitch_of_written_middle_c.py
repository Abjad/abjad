# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Bassoon_sounding_pitch_of_written_middle_c_01():

    bassoon = instrumenttools.Bassoon()

    assert bassoon.sounding_pitch_of_written_middle_c == "c'"
