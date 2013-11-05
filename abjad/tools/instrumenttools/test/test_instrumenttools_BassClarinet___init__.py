# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_BassClarinet___init___01():

    bass_clarinet = instrumenttools.BassClarinet()

    assert isinstance(bass_clarinet, instrumenttools.BassClarinet)
