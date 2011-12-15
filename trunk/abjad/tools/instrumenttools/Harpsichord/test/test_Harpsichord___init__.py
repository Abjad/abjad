from abjad import *


def test_Harpsichord___init___01():

    harpsichord = instrumenttools.Harpsichord()

    assert isinstance(harpsichord, instrumenttools.Harpsichord)
