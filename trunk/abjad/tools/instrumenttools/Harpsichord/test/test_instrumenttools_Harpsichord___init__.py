# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Harpsichord___init___01():

    harpsichord = instrumenttools.Harpsichord()

    assert isinstance(harpsichord, instrumenttools.Harpsichord)
