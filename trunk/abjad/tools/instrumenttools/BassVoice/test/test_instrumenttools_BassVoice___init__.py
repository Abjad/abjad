from abjad import *


def test_instrumenttools_BassVoice___init___01():

    voice = instrumenttools.BassVoice()

    assert isinstance(voice, instrumenttools.BassVoice)
