from abjad import *


def test_instrumenttools_BassSaxophone___init___01():

    bass_saxophone = instrumenttools.BassSaxophone()

    assert isinstance(bass_saxophone, instrumenttools.BassSaxophone)
