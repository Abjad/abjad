from abjad import *


def test_ComplexBeamSpanner___init___01():
    '''Init empty complex beam spanner.
    '''

    beam = spannertools.ComplexBeamSpanner()
    assert isinstance(beam, spannertools.ComplexBeamSpanner)


def test_ComplexBeamSpanner___init___02():

    staff = Staff("c'16 e'16 r16 f'16 g'2")
    spannertools.ComplexBeamSpanner(staff[:4])

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

    assert staff.format == "\\new Staff {\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #2\n\tc'16 [\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #2\n\te'16 ]\n\tr16\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #0\n\tf'16 [ ]\n\tg'2\n}"
