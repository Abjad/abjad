from abjad import *


def test_BeamSpanner___init___01():
    '''Init empty beam spanner.
    '''

    beam = spannertools.BeamSpanner()
    assert isinstance(beam, spannertools.BeamSpanner)


def test_BeamSpanner___init___02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.BeamSpanner(staff[:4])

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\tg'2\n}"
