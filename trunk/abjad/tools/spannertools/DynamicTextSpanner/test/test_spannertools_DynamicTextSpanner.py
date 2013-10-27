# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_DynamicTextSpanner_01():

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    dynamic_text_spanner = spannertools.DynamicTextSpanner(mark='f')
    dynamic_text_spanner.attach(voice[:2])
    dynamic_text_spanner = spannertools.DynamicTextSpanner(mark='p')
    dynamic_text_spanner.attach(voice[2:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \f
            d'8
            e'8 \p
            f'8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()
