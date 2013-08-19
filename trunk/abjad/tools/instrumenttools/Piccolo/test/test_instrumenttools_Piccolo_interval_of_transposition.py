# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Piccolo_interval_of_transposition_01():

    piccolo = instrumenttools.Piccolo()

    piccolo.interval_of_transposition == pitchtools.NamedMelodicInterval('+P8')
