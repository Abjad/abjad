from abjad import *


def test_markuptools_get_up_markup_attached_to_component_01():

    chord = Chord([-11, 2, 5], (1, 4))
    up_markup = markuptools.Markup('UP', 'up')(chord)
    down_markup = markuptools.Markup('DOWN', 'down')(chord)

    assert markuptools.get_up_markup_attached_to_component(chord) == (up_markup, )
