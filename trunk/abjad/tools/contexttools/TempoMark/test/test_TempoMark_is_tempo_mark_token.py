from abjad import *


def test_TempoMark_is_tempo_mark_token_01():

    tempo_mark = contexttools.TempoMark(Duration(1, 4), 72)

    assert tempo_mark.is_tempo_mark_token('Langsam')
    assert tempo_mark.is_tempo_mark_token((Duration(1, 8), 84))
    assert tempo_mark.is_tempo_mark_token(contexttools.TempoMark((1, 8), 96))
    assert tempo_mark.is_tempo_mark_token(('Vivce', (1, 8), 108))


def test_TempoMark_is_tempo_mark_token_02():

    tempo_mark = contexttools.TempoMark(Duration(1, 4), 72)

    assert not tempo_mark.is_tempo_mark_token(None)
    assert not tempo_mark.is_tempo_mark_token(13)
