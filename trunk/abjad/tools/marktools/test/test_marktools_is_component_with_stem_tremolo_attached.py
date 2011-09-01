from abjad import *


def test_marktools_is_component_with_stem_tremolo_attached_01():

    staff = Staff("c'2 d'2")
    marktools.StemTremolo(16)(staff[0])

    assert marktools.is_component_with_stem_tremolo_attached(staff[0])
    assert not marktools.is_component_with_stem_tremolo_attached(staff[1])
