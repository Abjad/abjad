from abjad import *


def test_tuplettools_move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet_01():
    '''Scale tuplet contents and then bequeath in-score position
        of tuplet to contents.'''

    t = Staff(tuplettools.FixedDurationTuplet(Duration(3, 8), "c'8 d'8") * 2)
    spannertools.BeamSpanner(t.leaves)

    r'''
    \new Staff {
        \fraction \times 3/2 {
            c'8 [
            d'8
        }
        \fraction \times 3/2 {
            c'8
            d'8 ]
        }
    }
    '''

    tuplettools.move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet(t[0])

    r'''
    \new Staff {
        c'8. [
        d'8.
        \fraction \times 3/2 {
            c'8
            d'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8. [\n\td'8.\n\t\\fraction \\times 3/2 {\n\t\tc'8\n\t\td'8 ]\n\t}\n}"


def test_tuplettools_move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet_02():
    '''Scale tuplet contents and then bequeath in-score position
        of tuplet to contents.'''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    tuplettools.move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet(t[0])

    r'''
    \new Voice {
        \times 2/3 {
            c'8
        }
        \times 2/3 {
            d'8
        }
        \times 2/3 {
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8\n\t}\n\t\\times 2/3 {\n\t\td'8\n\t}\n\t\\times 2/3 {\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t}\n}"
