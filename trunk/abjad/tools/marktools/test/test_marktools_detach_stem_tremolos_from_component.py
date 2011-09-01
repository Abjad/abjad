from abjad import *


def test_marktools_detach_stem_tremolos_from_component_01():

    note = Note("c'4")
    stem_tremolo = marktools.StemTremolo(16)(note)

    attached_stem_tremolo = marktools.get_stem_tremolo_attached_to_component(note)
    assert attached_stem_tremolo is stem_tremolo

    stem_tremolos = marktools.detach_stem_tremolos_attached_to_component(note)
    assert len(stem_tremolos) == 1
    assert stem_tremolos[0] is stem_tremolo
