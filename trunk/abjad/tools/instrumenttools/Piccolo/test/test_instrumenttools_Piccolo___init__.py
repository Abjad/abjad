from abjad import *


def test_instrumenttools_Piccolo___init___01():

    piccolo = instrumenttools.Piccolo()

    assert isinstance(piccolo, instrumenttools.Piccolo)
