from abjad import *


def test_marktools_get_marks_attached_to_components_in_expr_01():

    staff = Staff(r"c'4 \pp d' \staccato e' \ff f' \staccato")

    assert len(marktools.get_marks_attached_to_components_in_expr(staff)) == 4
