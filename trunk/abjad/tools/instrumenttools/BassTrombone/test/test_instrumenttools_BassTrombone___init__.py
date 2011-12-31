from abjad import *


def test_instrumenttools_BassTrombone___init___01():

    trombone = instrumenttools.BassTrombone()

    assert isinstance(trombone, instrumenttools.BassTrombone)
