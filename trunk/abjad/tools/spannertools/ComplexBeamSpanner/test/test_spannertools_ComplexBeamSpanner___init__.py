# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_ComplexBeamSpanner___init___01():
    r'''Init empty complex beam spanner.
    '''

    beam = spannertools.ComplexBeamSpanner()
    assert isinstance(beam, spannertools.ComplexBeamSpanner)


def test_spannertools_ComplexBeamSpanner___init___02():

    staff = Staff("c'16 e'16 r16 f'16 g'2")
    beam = spannertools.ComplexBeamSpanner()
    beam.attach(staff[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #2
            e'16 ]
            r16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 [ ]
            g'2
        }
        '''
        )
