from abjad import *


def test_marktools_is_component_with_articulation_attached_01():

    staff = Staff("c'2 d'2")
    marktools.Articulation('staccato')(staff[0])

    assert marktools.is_component_with_articulation_attached(staff[0])
    assert not marktools.is_component_with_articulation_attached(staff[1])
