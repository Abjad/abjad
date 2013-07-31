# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Cello_sounding_pitch_of_written_middle_c_01():

    cello = instrumenttools.Cello()

    assert cello.sounding_pitch_of_written_middle_c == "c'"
