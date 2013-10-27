# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_BassClarinet_sounding_pitch_of_written_middle_c_01():

    bass_clarinet = instrumenttools.BassClarinet()

    assert bass_clarinet.sounding_pitch_of_written_middle_c == 'bf,'
