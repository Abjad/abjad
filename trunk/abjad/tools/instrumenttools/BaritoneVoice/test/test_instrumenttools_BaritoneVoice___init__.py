from abjad import *


def test_instrumenttools_BaritoneVoice___init___01():

    voice = instrumenttools.BaritoneVoice()

    assert isinstance(voice, instrumenttools.BaritoneVoice)
