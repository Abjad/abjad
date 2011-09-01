from abjad import *


def test_marktools_get_stem_tremolos_attached_to_component_01():

    note = Note("c'4")
    stem_tremolo = marktools.StemTremolo(16)(note)
    stem_tremolos = marktools.get_stem_tremolos_attached_to_component(note)

    assert stem_tremolos[0] is stem_tremolo
