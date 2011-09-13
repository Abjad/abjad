from abjad import *


def test_NaturalHarmonic___init___01():
    '''Init natural harmonic from note.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    natural_harmonic = notetools.NaturalHarmonic(t[1])
    componenttools.move_parentage_and_spanners_from_components_to_components(t[1:2], [natural_harmonic])

    r'''
    \new Staff {
        c'8
        \once \override NoteHead #'style = #'harmonic
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff {\n\tc'8\n\t\\once \\override NoteHead #'style = #'harmonic\n\td'8\n\te'8\n\tf'8\n}"
