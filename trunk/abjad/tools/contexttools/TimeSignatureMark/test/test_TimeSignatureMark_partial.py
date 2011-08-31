from abjad import *


def test_TimeSignatureMark_partial_01():

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.TimeSignatureMark((2, 8), partial = Duration(1, 8))(t)

    r'''
    \new Staff {
        \partial 8
        \time 2/8
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t\\partial 8\n\t\\time 2/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_TimeSignatureMark_partial_02():
    '''Time signature partial is read / write.
    '''

    meter = contexttools.TimeSignatureMark((3, 8), partial = Duration(1, 8))
    assert meter.partial == Duration(1, 8)

    meter.partial = Duration(2, 8)
    assert meter.partial == Duration(2, 8)


def test_TimeSignatureMark_partial_03():
    '''Time signature partial can be cleared with none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
    time_signature = contexttools.TimeSignatureMark((4, 8))(staff)
    time_signature.partial = Duration(2, 8)

    r'''
    \new Staff {
        \partial 4
        \time 4/8
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
    }
    '''

    assert staff.format == "\\new Staff {\n\t\\partial 4\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n}"

    time_signature.partial = None

    r'''
    \new Staff {
        \time 4/8
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
    }
    '''

    assert staff.format == "\\new Staff {\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n}"
