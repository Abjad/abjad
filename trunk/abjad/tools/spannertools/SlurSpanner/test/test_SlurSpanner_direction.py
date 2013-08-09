# -*- encoding: utf-8 -*-
from abjad import *


def test_SlurSpanner_direction_01():
    voice = Voice("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(voice, direction=Up)

    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 ^ (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    assert more(voice).get_spanners() == set([slur])
