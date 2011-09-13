from abjad import *


def test_measuretools_extend_measures_in_expr_and_apply_full_measure_tuplets_to_measure_contents_01():

    staff = Staff([Measure((2, 8), "c'8 d'8"), Measure((3, 8), "e'8 f'8 g'8")])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 3/8
            e'8
            f'8
            g'8
        }
    }
    '''
    supplement = [Rest((1, 16))]
    r = measuretools.extend_measures_in_expr_and_apply_full_measure_tuplets_to_measure_contents(staff, supplement)

    r'''
    \new Staff {
        {
            \time 2/8
            \times 4/5 {
                c'8
                d'8
                r16
            }
        }
        {
            \time 3/8
            \fraction \times 6/7 {
                e'8
                f'8
                g'8
                r16
            }
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\times 4/5 {\n\t\t\tc'8\n\t\t\td'8\n\t\t\tr16\n\t\t}\n\t}\n\t{\n\t\t\\time 3/8\n\t\t\\fraction \\times 6/7 {\n\t\t\te'8\n\t\t\tf'8\n\t\t\tg'8\n\t\t\tr16\n\t\t}\n\t}\n}"
