# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Bassoon___init___01():

    bassoon = instrumenttools.Bassoon()

    assert isinstance(bassoon, instrumenttools.Bassoon)
