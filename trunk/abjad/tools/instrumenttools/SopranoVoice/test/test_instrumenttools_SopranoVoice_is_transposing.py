from abjad import *


def test_instrumenttools_SopranoVoice_is_transposing_01():

    voice = instrumenttools.SopranoVoice()

    assert not voice.is_transposing
