# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Tempo_is_tempo_mark_token_01():

    tempo_mark = Tempo(Duration(1, 4), 72)

    assert tempo_mark.is_tempo_mark_token('Langsam')
    assert tempo_mark.is_tempo_mark_token((Duration(1, 8), 84))
    assert tempo_mark.is_tempo_mark_token(Tempo((1, 8), 96))
    assert tempo_mark.is_tempo_mark_token(('Vivce', (1, 8), 108))


def test_marktools_Tempo_is_tempo_mark_token_02():

    tempo_mark = Tempo(Duration(1, 4), 72)

    assert not tempo_mark.is_tempo_mark_token(None)
    assert not tempo_mark.is_tempo_mark_token(13)
