from abjad import *


def test_instrumenttools_SopranoVoice_storage_format_01():

    voice = instrumenttools.SopranoVoice()

    assert voice.storage_format == 'instrumenttools.SopranoVoice()'
