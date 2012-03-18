from abjad import *


def test_instrumenttools_BassVoice_is_transposing_01():

    voice = instrumenttools.BassVoice()

    assert not voice.is_transposing
