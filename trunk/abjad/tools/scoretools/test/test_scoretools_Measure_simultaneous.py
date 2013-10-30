# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Measure_simultaneous_01():
    r'''Measures may be hold simultaneous contents.
    '''

    measure = Measure((2, 8), [])
    measure.append(Voice("c'8 d'8"))
    measure.append(Voice("e'8 f'8"))
    measure.is_simultaneous = True
    command = marktools.LilyPondCommandMark('voiceOne')
    attach(command, measure[0])
    command = marktools.LilyPondCommandMark('voiceTwo')
    attach(command, measure[1])
    staff = Staff([measure])

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()
