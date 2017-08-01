# -*- coding: utf-8 -*-
import abjad


def test_agenttools_InspectionAgent_get_markup_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    slur = abjad.Slur()
    abjad.attach(slur, staff[:])
    markup_1 = abjad.Markup('foo')
    abjad.attach(markup_1, staff[0])
    markup_2 = abjad.Markup('bar')
    abjad.attach(markup_2, staff[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 (
                - \markup {
                    \column
                        {
                            \line
                                {
                                    foo
                                }
                            \line
                                {
                                    bar
                                }
                        }
                    }
            d'8
            e'8
            f'8 )
        }
        '''
        )

    markup = abjad.inspect(staff[0]).get_markup()
    assert len(markup) == 2
    assert markup_1 in markup
    assert markup_2 in markup


def test_agenttools_InspectionAgent_get_markup_02():

    chord = abjad.Chord([-11, 2, 5], (1, 4))
    up_markup = abjad.Markup('UP', Up)
    abjad.attach(up_markup, chord)
    down_markup = abjad.Markup('DOWN', Down)
    abjad.attach(down_markup, chord)
    found_markup = abjad.inspect(chord).get_markup(direction=Down)
    assert found_markup == (down_markup,)


def test_agenttools_InspectionAgent_get_markup_03():

    chord = abjad.Chord([-11, 2, 5], (1, 4))
    up_markup = abjad.Markup('UP', Up)
    abjad.attach(up_markup, chord)
    down_markup = abjad.Markup('DOWN', Down)
    abjad.attach(down_markup, chord)
    found_markup = abjad.inspect(chord).get_markup(direction=Up)
    assert found_markup == (up_markup,)
