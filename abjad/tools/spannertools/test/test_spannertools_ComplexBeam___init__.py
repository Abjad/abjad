# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_ComplexBeam___init___01():
    r'''Initialize empty complex beam spanner.
    '''

    beam = spannertools.ComplexBeam()
    assert isinstance(beam, spannertools.ComplexBeam)


def test_spannertools_ComplexBeam___init___02():

    staff = Staff("c'16 e'16 r16 f'16 g'2")
    beam = spannertools.ComplexBeam()
    attach(beam, staff[:4])

    assert format(staff) == stringtools.normalize(
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
