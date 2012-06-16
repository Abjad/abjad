from abjad import *


def test_instrumenttools_BaritoneVoice_storage_format_01():

    voice = instrumenttools.BaritoneVoice()

    assert voice.storage_format == 'instrumenttools.BaritoneVoice()'
