from abjad import *


def test_instrumenttools_Vibraphone___init___01():

    vibraphone = instrumenttools.Vibraphone()

    assert isinstance(vibraphone, instrumenttools.Vibraphone)
