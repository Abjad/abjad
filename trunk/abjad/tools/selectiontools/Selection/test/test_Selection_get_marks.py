from abjad import *


def test_Selection_get_marks_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = contexttools.ClefMark('treble')(staff)
    dynamic = contexttools.DynamicMark('f')(staff[0])

    parentage = staff[0].select_parentage(include_self=True)
    context_marks = parentage.get_marks(
        mark_classes=contexttools.ContextMark,
        recurse=False,
        )

    assert len(context_marks) == 2
    assert clef in context_marks
    assert dynamic in context_marks
