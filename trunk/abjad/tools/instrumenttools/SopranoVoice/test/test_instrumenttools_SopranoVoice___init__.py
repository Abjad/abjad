from abjad import *


def test_instrumenttools_SopranoVoice___init___01():

    voice = instrumenttools.SopranoVoice()

    assert isinstance(voice, instrumenttools.SopranoVoice)
