from abjad import *


def test_componenttools_get_components_in_expr_with_name_01():

    staff = Staff(r"\new Voice { c'8 d'8 } \new Voice { e'8 f'8 } \new Voice { g'4 }")
    staff[0].name = 'outer voice'
    staff[1].name = 'middle voice'
    staff[2].name = 'outer voice'

    assert componenttools.get_components_in_expr_with_name(staff, 'outer voice') == [staff[0], staff[2]]
    assert componenttools.get_components_in_expr_with_name(staff, 'middle voice') == [staff[1]]
