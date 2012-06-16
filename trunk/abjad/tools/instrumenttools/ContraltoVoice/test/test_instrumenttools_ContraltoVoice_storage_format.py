from abjad import *


def test_instrumenttools_ContraltoVoice_storage_format_01():

    voice = instrumenttools.ContraltoVoice()

    assert voice.storage_format == 'instrumenttools.ContraltoVoice()'

