from abjad import *


def test_instrumenttools_ContraltoVoice_is_transposing_01():

    voice = instrumenttools.ContraltoVoice()

    assert not voice.is_transposing
