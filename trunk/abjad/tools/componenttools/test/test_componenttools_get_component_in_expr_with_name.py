from abjad import *
import py.test


def test_componenttools_get_component_in_expr_with_name_01():

    staff = Staff(r"\new Voice { c'8 d'8 } \new Voice { e'8 f'8 } \new Voice { g'4 }")
    staff[0].name = 'top voice'
    staff[1].name = 'middle voice'
    staff[2].name = 'bottom voice'

    assert componenttools.get_component_in_expr_with_name(staff, 'top voice') == staff[0]
    assert componenttools.get_component_in_expr_with_name(staff, 'middle voice') == staff[1]
    assert componenttools.get_component_in_expr_with_name(staff, 'bottom voice') == staff[2]


def test_componenttools_get_component_in_expr_with_name_02():

    staff = Staff(r"\new Voice { c'8 d'8 } \new Voice { e'8 f'8 } \new Voice { g'4 }")
    staff[0].name = 'outer voice'
    staff[1].name = 'middle voice'
    staff[2].name = 'outer voice'

    py.test.raises(ExtraNamedComponentError,
        "componenttools.get_component_in_expr_with_name(staff, 'outer voice')")
    py.test.raises(MissingNamedComponentError,
        "componenttools.get_component_in_expr_with_name(staff, 'no voice')")
