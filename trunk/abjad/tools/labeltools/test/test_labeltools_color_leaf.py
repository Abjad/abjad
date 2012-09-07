from abjad import *


def test_labeltools_color_leaf_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(staff.leaves)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    labeltools.color_leaf(staff[0], 'red')

    r'''
    \new Staff {
        \once \override Accidental #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\t\\once \\override Accidental #'color = #red\n\t\\once \\override Dots #'color = #red\n\t\\once \\override NoteHead #'color = #red\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
