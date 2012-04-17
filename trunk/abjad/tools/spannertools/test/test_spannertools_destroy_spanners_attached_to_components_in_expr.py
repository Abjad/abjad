from abjad import *


def test_spannertools_destroy_spanners_attached_to_components_in_expr_01():

    staff = Staff("c'4 [ d' ] e' ( f' ) ]")
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(staff)) == 2

    spannertools.destroy_spanners_attached_to_components_in_expr(staff)
    assert not spannertools.get_spanners_attached_to_any_improper_child_of_component(staff)
