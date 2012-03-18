from abjad import *


def test_instrumenttools_MezzoSopranoVoice___init___01():

    voice = instrumenttools.MezzoSopranoVoice()

    assert isinstance(voice, instrumenttools.MezzoSopranoVoice)
