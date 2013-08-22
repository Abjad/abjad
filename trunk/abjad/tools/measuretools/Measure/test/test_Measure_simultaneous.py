# -*- encoding: utf-8 -*-
from abjad import *


def test_Measure_simultaneous_01():
    r'''Measures may be hold simultaneous contents.
    '''

    measure = Measure((2, 8), Voice(notetools.make_repeated_notes(2)) * 2)
    measure.is_simultaneous = True
    marktools.LilyPondCommandMark('voiceOne')(measure[0])
    marktools.LilyPondCommandMark('voiceTwo')(measure[1])

    staff = Staff([measure])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

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

    assert inspect(staff).is_well_formed()
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
