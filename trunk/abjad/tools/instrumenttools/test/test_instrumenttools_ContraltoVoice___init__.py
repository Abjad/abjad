# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_ContraltoVoice___init___01():

    voice = instrumenttools.ContraltoVoice()

    assert isinstance(voice, instrumenttools.ContraltoVoice)
