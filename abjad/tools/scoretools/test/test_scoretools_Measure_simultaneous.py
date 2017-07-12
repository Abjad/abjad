# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Measure_simultaneous_01():
    r'''Measures may be hold simultaneous contents.
    '''

    measure = abjad.Measure((2, 8), [])
    measure.append(abjad.Voice("c'8 d'8"))
    measure.append(abjad.Voice("e'8 f'8"))
    measure.is_simultaneous = True
    command = abjad.LilyPondCommand('voiceOne')
    abjad.attach(command, measure[0])
    command = abjad.LilyPondCommand('voiceTwo')
    abjad.attach(command, measure[1])
    staff = abjad.Staff([measure])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            <<
                \time 2/8
                \new Voice {
                    \voiceOne
                    c'8
                    d'8
                }
                \new Voice {
                    \voiceTwo
                    e'8
                    f'8
                }
            >>
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
