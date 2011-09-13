from abjad import *


def test_HairpinSpanner_stop_dynamic_string_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')

    r'''
    \new Staff {
        c'8 \< \p
        d'8
        e'8
        f'8 \f
    }
    '''

    assert hairpin.stop_dynamic_string == 'f'
    assert staff.format == "\\new Staff {\n\tc'8 \\< \\p\n\td'8\n\te'8\n\tf'8 \\f\n}"

    hairpin.stop_dynamic_string = 'mf'

    r'''
    \new Staff {
        c'8 \< \p
        d'8
        e'8
        f'8 \mf
    }
    '''

    assert hairpin.stop_dynamic_string == 'mf'
    assert staff.format == "\\new Staff {\n\tc'8 \\< \\p\n\td'8\n\te'8\n\tf'8 \\mf\n}"
