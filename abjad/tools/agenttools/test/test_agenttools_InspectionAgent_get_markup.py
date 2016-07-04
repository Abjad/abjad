# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_get_markup_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff[:])
    markup_1 = markuptools.Markup('foo')
    attach(markup_1, staff[0])
    markup_2 = markuptools.Markup('bar')
    attach(markup_2, staff[0])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 (
                - \markup {
                    \column
                        {
                            foo
                            bar
                        }
                    }
            d'8
            e'8
            f'8 )
        }
        '''
        )

    markup = inspect_(staff[0]).get_markup()
    assert len(markup) == 2
    assert markup_1 in markup
    assert markup_2 in markup


def test_agenttools_InspectionAgent_get_markup_02():

    chord = Chord([-11, 2, 5], (1, 4))
    up_markup = markuptools.Markup('UP', Up)
    attach(up_markup, chord)
    down_markup = markuptools.Markup('DOWN', Down)
    attach(down_markup, chord)
    found_markup = inspect_(chord).get_markup(direction=Down)
    assert found_markup == (down_markup,)


def test_agenttools_InspectionAgent_get_markup_03():

    chord = Chord([-11, 2, 5], (1, 4))
    up_markup = markuptools.Markup('UP', Up)
    attach(up_markup, chord)
    down_markup = markuptools.Markup('DOWN', Down)
    attach(down_markup, chord)
    found_markup = inspect_(chord).get_markup(direction=Up)
    assert found_markup == (up_markup,)