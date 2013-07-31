# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_BFlatClarinet_sounding_pitch_of_written_middle_c_01():

    clarinet = instrumenttools.BFlatClarinet()

    assert clarinet.sounding_pitch_of_written_middle_c == 'bf'
