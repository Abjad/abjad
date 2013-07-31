# -*- encoding: utf-8 -*-
from abjad import *


def test_Component_get_markup_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.select_leaves())
    markup_1 = markuptools.Markup('foo')(staff[0])
    markup_2 = markuptools.Markup('bar')(staff[0])

    r'''
    \new Staff {
        c'8 - \markup { \column { foo bar } } (
        d'8
        e'8
        f'8 )
    }
    '''

    markup = staff[0].get_markup()

    assert len(markup) == 2
    assert markup_1 in markup
    assert markup_2 in markup


def test_Component_get_markup_02():

    chord = Chord([-11, 2, 5], (1, 4))
    up_markup = markuptools.Markup('UP', Up)(chord)
    down_markup = markuptools.Markup('DOWN', Down)(chord)
    found_markup = chord.get_markup(direction=Down)
    assert found_markup == (down_markup,) 


def test_Component_get_markup_03():

    chord = Chord([-11, 2, 5], (1, 4))
    up_markup = markuptools.Markup('UP', Up)(chord)
    down_markup = markuptools.Markup('DOWN', Down)(chord)
    found_markup = chord.get_markup(direction=Up)
    assert found_markup == (up_markup,)
