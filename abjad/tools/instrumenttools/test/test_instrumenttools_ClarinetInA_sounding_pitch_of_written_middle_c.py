# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_ClarinetInA_sounding_pitch_of_written_middle_c_01():

    clarinet = instrumenttools.ClarinetInA()

    assert clarinet.sounding_pitch_of_written_middle_c == 'a'
