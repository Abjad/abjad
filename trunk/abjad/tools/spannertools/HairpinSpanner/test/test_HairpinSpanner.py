from abjad import *
from abjad.checks import IntermarkedHairpinCheck
from abjad.checks import ShortHairpinCheck
import py.test


def test_HairpinSpanner_01():
    '''Hairpins span adjacent leaves.'''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.CrescendoSpanner(t[:4])

    r'''
    \new Staff {
        c'8 \<
        cs'8
        d'8
        ef'8 \!
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_HairpinSpanner_02():
    '''Hairpins spanning a single leaf are allowed but not well-formed.'''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.CrescendoSpanner(t[0:1])
    checker = ShortHairpinCheck()

    r'''
    \new Staff {
        c'8 \< \!
        cs'8
        d'8
        ef'8
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert not checker.check(t)
    assert t.format == "\\new Staff {\n\tc'8 \\< \\!\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_HairpinSpanner_03():
    '''Hairpins and dynamics apply separately.'''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.CrescendoSpanner(t[:4])
    contexttools.DynamicMark('p')(t[0])
    contexttools.DynamicMark('f')(t[3])

    r'''
    \new Staff {
        c'8 \p \<
        cs'8
        d'8
        ef'8 \f
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 \\p \\<\n\tcs'8\n\td'8\n\tef'8 \\f\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_HairpinSpanner_04():
    '''Internal marks raise well-formedness error.'''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.CrescendoSpanner(t[:4])
    assert py.test.raises(WellFormednessError, "contexttools.DynamicMark('p')(t[2])")


def test_HairpinSpanner_05():
    '''Apply back-to-back hairpins separately.'''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    contexttools.DynamicMark('p')(t[0])
    spannertools.CrescendoSpanner(t[0:3])
    contexttools.DynamicMark('f')(t[2])
    spannertools.DecrescendoSpanner(t[2:5])
    contexttools.DynamicMark('p')(t[4])
    spannertools.CrescendoSpanner(t[4:7])
    contexttools.DynamicMark('f')(t[6])

    r'''
    \new Staff {
        c'8 \p \<
        cs'8
        d'8 \f \>
        ef'8
        e'8 \p \<
        f'8
        fs'8 \f
        g'8
    }
    '''

    assert t.format == "\\new Staff {\n\tc'8 \\p \\<\n\tcs'8\n\td'8 \\f \\>\n\tef'8\n\te'8 \\p \\<\n\tf'8\n\tfs'8 \\f\n\tg'8\n}"
    assert componenttools.is_well_formed_component(t)


def test_HairpinSpanner_06():
    '''Hairpins format rests.'''

    t = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
    spannertools.CrescendoSpanner(t[:])


    r'''
    \new Staff {
        r8 \<
        r8
        r8
        r8
        e'8
        f'8
        fs'8
        g'8 \!
    }
    '''

    assert t.format == "\\new Staff {\n\tr8 \\<\n\tr8\n\tr8\n\tr8\n\te'8\n\tf'8\n\tfs'8\n\tg'8 \\!\n}"
    assert componenttools.is_well_formed_component(t)


def test_HairpinSpanner_07():
    '''Trim hairpins with dynamic marks behave as expected.'''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    rest = Rest(t[0])
    componenttools.move_parentage_and_spanners_from_components_to_components(t[0:1], [rest])
    rest = Rest(t[-1])
    componenttools.move_parentage_and_spanners_from_components_to_components(t[-1:], [rest])
    spannertools.HairpinSpanner(t.leaves, 'p < f', include_rests = False)

    spanner = spannertools.get_the_only_spanner_attached_to_component(
        t[0], spannertools.HairpinSpanner)
    assert len(spanner.components) == len(t)
    assert t.format == "\\new Staff {\n\tr8\n\tcs'8 \\< \\p\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8 \\f\n\tr8\n}"
    checker = IntermarkedHairpinCheck()
    assert checker.check(t)

    r'''
    \new Staff {
        r8
        cs'8 \< \p
        d'8
        ef'8
        e'8
        f'8
        fs'8 \f
        r8
    }
    '''
