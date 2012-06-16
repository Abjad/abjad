from abjad import *


def test_BendAfter_format_01():
    '''Bend formats correctly on notes.
    '''

    t = Note("cs'4")
    marktools.BendAfter(8)(t)
    assert t.lilypond_format == "cs'4 - \\bendAfter #'8.0"
    marktools.detach_articulations_attached_to_component(t)
    assert t.lilypond_format == "cs'4"


def test_BendAfter_format_02():
    '''Bend formats correctly on chords.
    '''

    t = Chord([1, 2, 3], (1, 4))
    marktools.BendAfter(8)(t)
    assert t.lilypond_format == "<cs' d' ef'>4 - \\bendAfter #'8.0"
    marktools.detach_articulations_attached_to_component(t)
    assert t.lilypond_format == "<cs' d' ef'>4"


def test_BendAfter_format_03():
    '''Bend formats correctly on rests.
    '''

    t = Rest((1, 4))
    marktools.BendAfter(8)(t)
    assert t.lilypond_format == "r4 - \\bendAfter #'8.0"
    marktools.detach_articulations_attached_to_component(t)
    assert t.lilypond_format == "r4"
