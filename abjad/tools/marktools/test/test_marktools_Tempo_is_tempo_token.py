# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Tempo_is_tempo_token_01():

    tempo = Tempo(Duration(1, 4), 72)

    assert tempo.is_tempo_token('Langsam')
    assert tempo.is_tempo_token((Duration(1, 8), 84))
    assert tempo.is_tempo_token(Tempo((1, 8), 96))
    assert tempo.is_tempo_token(('Vivce', (1, 8), 108))


def test_marktools_Tempo_is_tempo_token_02():

    tempo = Tempo(Duration(1, 4), 72)

    assert not tempo.is_tempo_token(None)
    assert not tempo.is_tempo_token(13)
