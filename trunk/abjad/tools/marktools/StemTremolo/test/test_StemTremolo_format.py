from abjad import *


def test_StemTremolo_format_01():
    '''Tremolo formats correctly on notes.
    '''

    t = Note("cs'4")
    marktools.StemTremolo(8)(t)
    assert t.format == "cs'4 :8"
    marktools.detach_stem_tremolos_attached_to_component(t)
    assert t.format == "cs'4"


def test_StemTremolo_format_02():
    '''Tremolo formats correctly on chords.
    '''

    t = Chord([1, 2, 3], (1, 4))
    marktools.StemTremolo(8)(t)
    assert t.format == "<cs' d' ef'>4 :8"
    marktools.detach_stem_tremolos_attached_to_component(t)
    assert t.format == "<cs' d' ef'>4"


def test_StemTremolo_format_03():
    '''Tremolo formats correctly on rests.
    '''

    t = Rest((1, 4))
    marktools.StemTremolo(8)(t)
    assert t.format == "r4 :8"
    marktools.detach_stem_tremolos_attached_to_component(t)
    assert t.format == "r4"
