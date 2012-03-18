from abjad import *


def test_instrumenttools_MezzoSopranoVoice_is_transposing_01():

    voice = instrumenttools.MezzoSopranoVoice()

    assert not voice.is_transposing
