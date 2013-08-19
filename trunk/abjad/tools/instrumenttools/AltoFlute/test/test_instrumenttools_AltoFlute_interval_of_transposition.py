# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_AltoFlute_interval_of_transposition_01():

    alto_flute = instrumenttools.AltoFlute()

    assert alto_flute.interval_of_transposition == pitchtools.NamedMelodicInterval('-P4')
