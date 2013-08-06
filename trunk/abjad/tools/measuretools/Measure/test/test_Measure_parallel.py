# -*- encoding: utf-8 -*-
from abjad import *


def test_Measure_parallel_01():
    r'''Rigid measures may be hold parallel contents.
    '''

    measure = Measure((2, 8), Voice(notetools.make_repeated_notes(2)) * 2)
    measure.is_parallel = True
    marktools.LilyPondCommandMark('voiceOne')(measure[0])
    marktools.LilyPondCommandMark('voiceTwo')(measure[1])

    t = Staff([measure])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

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

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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
