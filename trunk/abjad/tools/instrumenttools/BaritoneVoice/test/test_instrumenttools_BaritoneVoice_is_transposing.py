from abjad import *


def test_instrumenttools_BaritoneVoice_is_transposing_01():

    voice = instrumenttools.BaritoneVoice()

    assert not voice.is_transposing
