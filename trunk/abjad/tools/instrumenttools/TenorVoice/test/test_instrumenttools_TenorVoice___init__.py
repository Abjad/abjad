from abjad import *


def test_instrumenttools_TenorVoice___init___01():

    voice = instrumenttools.TenorVoice()

    assert isinstance(voice, instrumenttools.TenorVoice)
