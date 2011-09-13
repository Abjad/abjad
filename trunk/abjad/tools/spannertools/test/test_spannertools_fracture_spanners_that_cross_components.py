from abjad import *
import py.test


def test_spannertools_fracture_spanners_that_cross_components_01():
    '''Fracture all spanners to the left of the leftmost component in list;
        fracture all spanners to the right of the rightmost component in list.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    spannertools.fracture_spanners_that_cross_components(t[1:3])

    r'''
    \new Staff {
        c'8 [ ]
        d'8 [
        e'8 ]
        f'8 [ ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [ ]\n\td'8 [\n\te'8 ]\n\tf'8 [ ]\n}"


def test_spannertools_fracture_spanners_that_cross_components_02():
    '''Fracture to the left of leftmost component;
        fracture to the right of rightmost component.'''

    t = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    spannertools.fracture_spanners_that_cross_components(t[1:2])

    r'''
    \new Staff {
        c'8 [ ]
        d'8 [ ]
        e'8 [
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 [ ]\n\td'8 [ ]\n\te'8 [\n\tf'8 ]\n}"


def test_spannertools_fracture_spanners_that_cross_components_03():
    '''Empty list raises no exception.'''

    result = spannertools.fracture_spanners_that_cross_components([])
    assert result == []


def test_spannertools_fracture_spanners_that_cross_components_04():
    '''Fractures around components at only top level of list.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.CrescendoSpanner(t)
    spannertools.BeamSpanner(t[:])

    r'''
    \new Staff {
        {
            c'8 [ \<
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ] \!
        }
    }
    '''

    spannertools.fracture_spanners_that_cross_components(t[1:2])

    r'''
    \new Staff {
        {
            c'8 [ \<
            d'8 ]
        }
        {
            e'8 [
            f'8 ]
        }
        {
            g'8 [
            a'8 ] \!
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [ \\<\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ] \\!\n\t}\n}"


def test_spannertools_fracture_spanners_that_cross_components_05():
    '''Fractures around components at only top level of list.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.CrescendoSpanner(t)
    spannertools.BeamSpanner(t[:])
    spannertools.TrillSpanner(t.leaves)

    r'''
    \new Staff {
        {
            c'8 [ \< \startTrillSpan
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ] \! \stopTrillSpan
        }
    }
    '''

    spannertools.fracture_spanners_that_cross_components(t[1:2])

    r'''
    \new Staff {
        {
            c'8 [ \< \startTrillSpan
            d'8 ]
        }
        {
            e'8 [
            f'8 ]
        }
        {
            g'8 [
            a'8 ] \! \stopTrillSpan
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [ \\< \\startTrillSpan\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ] \\! \\stopTrillSpan\n\t}\n}"
