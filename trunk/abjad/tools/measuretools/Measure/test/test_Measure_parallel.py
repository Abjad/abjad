from abjad import *


def test_Measure_parallel_01():
    '''Rigid measures may be hold parallel contents.
    '''

    measure = Measure((2, 8), Voice(notetools.make_repeated_notes(2)) * 2)
    measure.is_parallel = True
    marktools.LilyPondCommandMark('voiceOne')(measure[0])
    marktools.LilyPondCommandMark('voiceTwo')(measure[1])

    t = Staff([measure])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t<<\n\t\t\\time 2/8\n\t\t\\new Voice {\n\t\t\t\\voiceOne\n\t\t\tc'8\n\t\t\td'8\n\t\t}\n\t\t\\new Voice {\n\t\t\t\\voiceTwo\n\t\t\te'8\n\t\t\tf'8\n\t\t}\n\t>>\n}"
