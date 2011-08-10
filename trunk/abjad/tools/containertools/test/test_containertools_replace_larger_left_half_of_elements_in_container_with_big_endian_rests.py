from abjad import *


def test_containertools_replace_larger_left_half_of_elements_in_container_with_big_endian_rests_01( ):
    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8 d''8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
        b'8
        c''8
        d''8
    }
    '''

    containertools.replace_larger_left_half_of_elements_in_container_with_big_endian_rests(staff)

    r'''
    \new Staff {
        r2
        r8
        a'8
        b'8
        c''8
        d''8
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tr2\n\tr8\n\ta'8\n\tb'8\n\tc''8\n\td''8\n}"
