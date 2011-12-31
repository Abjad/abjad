from abjad import *


def test_instrumenttools_TenorTrombone___init___01():

    trombone = instrumenttools.TenorTrombone()

    assert isinstance(trombone, instrumenttools.TenorTrombone)
