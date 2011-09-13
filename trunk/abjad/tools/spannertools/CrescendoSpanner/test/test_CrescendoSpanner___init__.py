from abjad import *


def test_CrescendoSpanner___init___01():
    '''Init empty crescendo spanner.
    '''

    crescendo = spannertools.CrescendoSpanner()
    assert isinstance(crescendo, spannertools.CrescendoSpanner)


def test_CrescendoSpanner___init___02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.CrescendoSpanner(staff[:4])

    r'''
    \new Staff {
        c'8 \<
        d'8
        e'8
        f'8 \!
        g'2
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 \\<\n\td'8\n\te'8\n\tf'8 \\!\n\tg'2\n}"
