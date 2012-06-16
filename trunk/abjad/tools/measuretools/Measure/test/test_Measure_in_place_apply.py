from abjad import *


# TODO: move to test_Measure___init__.py

def test_Measure_in_place_apply_01():

    t = Voice([Note(n, (1, 8)) for n in range(8)])
    leaves_before = t.leaves
    Measure((4, 8), t[0:4])
    leaves_after = t.leaves

    r'''
    \new Voice {
        {
            \time 4/8
            c'8
            cs'8
            d'8
            ef'8
        }
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\t\\time 4/8\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t}\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_Measure_in_place_apply_02():

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    leaves_before = t.leaves
    Measure((4, 8), t[0:4])
    leaves_after = t.leaves

    r'''
    \new Staff {
        {
            \time 4/8
            c'8
            cs'8
            d'8
            ef'8
        }
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 4/8\n\t\tc'8\n\t\tcs'8\n\t\td'8\n\t\tef'8\n\t}\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_Measure_in_place_apply_03():

    t = Staff([Note(n, (1, 1)) for n in range(4)])
    leaves_before = t.leaves
    Measure((1, 1), t[0:1])
    leaves_after = t.leaves

    r'''
    \new Staff {
        {
            \time 1/1
            c'1
        }
        cs'1
        d'1
        ef'1
    }
    '''

    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/1\n\t\tc'1\n\t}\n\tcs'1\n\td'1\n\tef'1\n}"


def test_Measure_in_place_apply_04():

    t = Staff([Note(n, (1, 1)) for n in range(4)])
    Measure((1, 1), t[:1])
    Measure((1, 1), t[1:2])
    Measure((1, 1), t[2:3])
    Measure((1, 1), t[3:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 1/1
            c'1
        }
        {
            \time 1/1
            cs'1
        }
        {
            \time 1/1
            d'1
        }
        {
            \time 1/1
            ef'1
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/1\n\t\tc'1\n\t}\n\t{\n\t\t\\time 1/1\n\t\tcs'1\n\t}\n\t{\n\t\t\\time 1/1\n\t\td'1\n\t}\n\t{\n\t\t\\time 1/1\n\t\tef'1\n\t}\n}"
