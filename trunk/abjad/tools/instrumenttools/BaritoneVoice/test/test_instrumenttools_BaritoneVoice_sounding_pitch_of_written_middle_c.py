# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_BaritoneVoice_sounding_pitch_of_written_middle_c_01():

    voice = instrumenttools.BaritoneVoice()

    assert voice.sounding_pitch_of_written_middle_c == "c'"
