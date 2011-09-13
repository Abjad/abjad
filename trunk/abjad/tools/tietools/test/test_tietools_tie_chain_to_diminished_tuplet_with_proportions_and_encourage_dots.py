from abjad import *


def test_tietools_tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots_01():

    t = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
    tietools.TieSpanner(t[:2])
    spannertools.BeamSpanner(t[:])

    r'''
    \new Staff {
        c'8 [ ~
        c'16
        c'16 ]
    }
    '''

    tietools.tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots(
        tietools.get_tie_chain(t[0]), [1])

    r'''
    \new Staff {
        {
            c'8. [
        }
        c'16 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\tc'8. [\n\t}\n\tc'16 ]\n}"


def test_tietools_tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots_02():

    t = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
    tietools.TieSpanner(t[:2])
    spannertools.BeamSpanner(t[:])
    tietools.tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots(
        tietools.get_tie_chain(t[0]), [1, 2])

    r'''
    \new Staff {
        {
            c'16
            c'8
        }
        c'16 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\tc'16 [\n\t\tc'8\n\t}\n\tc'16 ]\n}"


def test_tietools_tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots_03():

    t = Staff([Note(0, (1, 8)), Note(0, (1, 16)), Note(0, (1, 16))])
    tietools.TieSpanner(t[:2])
    spannertools.BeamSpanner(t[:])
    tietools.tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots(
        tietools.get_tie_chain(t[0]), [1, 2, 2])

    r'''
    \new Staff {
        \times 4/5 {
            c'32. [
            c'16.
            c'16.
        }
        c'16 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t\\times 4/5 {\n\t\tc'32. [\n\t\tc'16.\n\t\tc'16.\n\t}\n\tc'16 ]\n}"
