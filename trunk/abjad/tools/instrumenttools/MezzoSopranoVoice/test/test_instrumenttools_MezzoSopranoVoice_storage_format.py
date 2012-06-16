from abjad import *


def test_instrumenttools_MezzoSopranoVoice_storage_format_01():

    voice = instrumenttools.MezzoSopranoVoice()

    assert voice.storage_format == 'instrumenttools.MezzoSopranoVoice()'
