from abjad import *


def test_instrumenttools_BaritoneSaxophone___init___01():

    baritone_saxophone = instrumenttools.BaritoneSaxophone()

    assert isinstance(baritone_saxophone, instrumenttools.BaritoneSaxophone)
