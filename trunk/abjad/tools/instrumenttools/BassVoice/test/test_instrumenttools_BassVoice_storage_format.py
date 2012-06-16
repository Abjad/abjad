from abjad import *


def test_instrumenttools_BassVoice_storage_format_01():

    voice = instrumenttools.BassVoice()

    assert voice.storage_format == 'instrumenttools.BassVoice()'
