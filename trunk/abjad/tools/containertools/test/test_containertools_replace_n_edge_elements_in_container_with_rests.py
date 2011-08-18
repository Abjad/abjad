from abjad import *


def test_containertools_replace_n_edge_elements_in_container_with_rests_01():
    '''For positive n, replace first n elements in container with big-endian rests.'''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
    }
    '''

    containertools.replace_n_edge_elements_in_container_with_rests(staff, 5)

    r'''
    \new Staff {
        r2
        r8
        a'8
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tr2\n\tr8\n\ta'8\n}"


def test_containertools_replace_n_edge_elements_in_container_with_rests_02():
    '''For negative n replace last n elements in container with little-endian rests.'''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
    }
    '''

    containertools.replace_n_edge_elements_in_container_with_rests(staff, -5)

    r'''
    \new Staff {
        c'8
        r8
        r2
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8\n\tr8\n\tr2\n}"
