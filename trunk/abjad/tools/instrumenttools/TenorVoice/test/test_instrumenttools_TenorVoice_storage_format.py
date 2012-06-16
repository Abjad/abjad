from abjad import *


def test_instrumenttools_TenorVoice_storage_format_01():

    voice = instrumenttools.TenorVoice()

    assert voice.storage_format == 'instrumenttools.TenorVoice()'
