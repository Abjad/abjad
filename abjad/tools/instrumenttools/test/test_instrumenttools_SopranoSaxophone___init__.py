# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_SopranoSaxophone___init___01():

    soprano_saxophone = instrumenttools.SopranoSaxophone()

    assert isinstance(soprano_saxophone, instrumenttools.SopranoSaxophone)
