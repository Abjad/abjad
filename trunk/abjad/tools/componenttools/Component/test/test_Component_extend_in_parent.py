from abjad import *


def test_Component_extend_in_parent_01():

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])

    result = t[-1].extend_in_parent(
        [Note("c'8"), Note("d'8"), Note("e'8")], 
        grow_spanners=True,
        )

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        c'8
        d'8
        e'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert result == t[-4:]
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tc'8\n\td'8\n\te'8 ]\n}"


def test_Component_extend_in_parent_02():
    '''Splice leaf after interior leaf.
    '''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    result = t[1].extend_in_parent([Note(2.5, (1, 8))], grow_spanners=True)

    r'''
    \new Voice {
        c'8 [
        d'8
        dqs'8
        e'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\tdqs'8\n\te'8 ]\n}"
    assert result == t[1:3]


def test_Component_extend_in_parent_03():
    '''Splice tuplet after tuplet.
    '''

    t = Voice([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
    spannertools.BeamSpanner(t[0])

    result = t[-1].extend_in_parent(
        [tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")], 
        grow_spanners=True,
        )

    r'''
    \new Voice {
        \times 2/3 {
            c'8 [
            d'8
            e'8
        }
        \times 2/3 {
            c'8
            d'8
            e'8 ]
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert result == t[:]
    assert t.lilypond_format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8 ]\n\t}\n}"


def test_Component_extend_in_parent_04():
    '''Splice after container with underspanners.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    spannertools.BeamSpanner(t.select_leaves())

    result = t[0].extend_in_parent([Note(2.5, (1, 8))], grow_spanners=True)

    r'''
    \new Voice {
        {
            c'8 [
            c'8
        }
        dqs'8
        {
            c'8
            c'8 ]
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\tc'8\n\t}\n\tdqs'8\n\t{\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
    assert result == t[0:2]


def test_Component_extend_in_parent_05():
    '''Extend leaves rightwards after leaf.
    '''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])

    result = t[-1].extend_in_parent(
        [Note("c'8"), Note("d'8"), Note("e'8")], 
        grow_spanners=False,
        )

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
        c'8
        d'8
        e'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert result == t[-4:]
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n\tc'8\n\td'8\n\te'8\n}"


def test_Component_extend_in_parent_06():
    '''Extend leaf rightwards after interior leaf.
    '''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])

    result = t[1].extend_in_parent([Note(2.5, (1, 8))], grow_spanners=False)

    r'''
    \new Voice {
        c'8 [
        d'8
        dqs'8
        e'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\tdqs'8\n\te'8 ]\n}"
    assert result == t[1:3]


### FIX FROM HERE DOWN ###

def test_Component_extend_in_parent_07():
    '''Splice leaves left of leaf.
    '''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16")]

    result = t[0].extend_in_parent(notes, direction=Left, grow_spanners=True)

    r'''
    \new Voice {
        c'16 [
        d'16
        e'16
        c'8
        d'8
        e'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert result == t[:4]
    assert t.lilypond_format == "\\new Voice {\n\tc'16 [\n\td'16\n\te'16\n\tc'8\n\td'8\n\te'8 ]\n}"


def test_Component_extend_in_parent_08():
    '''Splice leaf left of interior leaf.
    '''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])

    result = t[1].extend_in_parent(
        [Note(1.5, (1, 8))], 
        direction=Left, 
        grow_spanners=True,
        )

    r'''
    \new Voice {
        c'8 [
        dqf'8
        d'8
        e'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\tdqf'8\n\td'8\n\te'8 ]\n}"
    assert result == t[1:3]


def test_Component_extend_in_parent_09():
    '''Splice tuplet left of tuplet.
    '''

    t = Voice([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
    spannertools.BeamSpanner(t[0])

    result = t[0].extend_in_parent(
        [tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")], 
        direction=Left,
        grow_spanners=True,
        )

    r'''
    \new Voice {
        \times 2/3 {
            c'8 [
            d'8
            e'8
        }
        \times 2/3 {
            c'8
            d'8
            e'8 ]
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert result == t[:]
    assert t.lilypond_format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8 ]\n\t}\n}"


def test_Component_extend_in_parent_10():
    '''Splice left of container with underspanners.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t.select_leaves())

    result = t[1].extend_in_parent(
        [Note(2.5, (1, 8))], 
        direction=Left,
        grow_spanners=True,
        )

    r'''
    \new Voice {
        {
            c'8 [
            d'8
        }
        dqs'8
        {
            e'8
            f'8 ]
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\tdqs'8\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
    assert result == t[1:]


def test_Component_extend_in_parent_11():
    '''Extend leaves leftwards of leaf. Do not extend edge spanners.
    '''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16")]
    result = t[0].extend_in_parent(
        notes,
        direction=Left,
        grow_spanners=False,
        )

    r'''
    \new Voice {
        c'16
        d'16
        e'16
        c'8 [
        d'8
        e'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert result == t[:4]
    assert t.lilypond_format == "\\new Voice {\n\tc'16\n\td'16\n\te'16\n\tc'8 [\n\td'8\n\te'8 ]\n}"


def test_Component_extend_in_parent_12():
    '''Extend leaf leftwards of interior leaf. Do extend interior spanners.
    '''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    result = t[1].extend_in_parent(
        [Note(1.5, (1, 8))], 
        direction=Left,
        grow_spanners=False,
        )

    r'''
    \new Voice {
        c'8 [
        dqf'8
        d'8
        e'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\tdqf'8\n\td'8\n\te'8 ]\n}"
    assert result == t[1:3]
