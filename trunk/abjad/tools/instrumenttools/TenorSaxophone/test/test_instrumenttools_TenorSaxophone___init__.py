from abjad import *


def test_instrumenttools_TenorSaxophone___init___01():

    tenor_saxophone = instrumenttools.TenorSaxophone()

    assert isinstance(tenor_saxophone, instrumenttools.TenorSaxophone)
