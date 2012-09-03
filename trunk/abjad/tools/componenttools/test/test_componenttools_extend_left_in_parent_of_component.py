from abjad import *


def test_componenttools_extend_left_in_parent_of_component_01():
    '''Splice leaves left of leaf.'''

    t = Voice("c'8 d'8 e'8")
    beamtools.BeamSpanner(t[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16")]
    result = componenttools.extend_left_in_parent_of_component(t[0], notes, grow_spanners=True)

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

    assert componenttools.is_well_formed_component(t)
    assert result == t[:4]
    assert t.lilypond_format == "\\new Voice {\n\tc'16 [\n\td'16\n\te'16\n\tc'8\n\td'8\n\te'8 ]\n}"


def test_componenttools_extend_left_in_parent_of_component_02():
    '''Splice leaf left of interior leaf.'''

    t = Voice("c'8 d'8 e'8")
    beamtools.BeamSpanner(t[:])
    result = componenttools.extend_left_in_parent_of_component(
        t[1], [Note(1.5, (1, 8))], grow_spanners=True)

    r'''
    \new Voice {
        c'8 [
        dqf'8
        d'8
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\tdqf'8\n\td'8\n\te'8 ]\n}"
    assert result == t[1:3]


def test_componenttools_extend_left_in_parent_of_component_03():
    '''Splice tuplet left of tuplet.'''

    t = Voice([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
    beamtools.BeamSpanner(t[0])
    result = componenttools.extend_left_in_parent_of_component(
        t[0], [tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")], grow_spanners=True)

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

    assert componenttools.is_well_formed_component(t)
    assert result == t[:]
    assert t.lilypond_format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8 ]\n\t}\n}"


def test_componenttools_extend_left_in_parent_of_component_04():
    '''Splice left of container with underspanners.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beamtools.BeamSpanner(t.leaves)
    result = componenttools.extend_left_in_parent_of_component(
        t[1], [Note(2.5, (1, 8))], grow_spanners=True)

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

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\tdqs'8\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
    assert result == t[1:]


def test_componenttools_extend_left_in_parent_of_component_05():
    '''Extend leaves leftwards of leaf. Do not extend edge spanners.'''

    t = Voice("c'8 d'8 e'8")
    beamtools.BeamSpanner(t[:])
    notes = [Note("c'16"), Note("d'16"), Note("e'16")]
    result = componenttools.extend_left_in_parent_of_component(t[0], notes, grow_spanners=False)

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

    assert componenttools.is_well_formed_component(t)
    assert result == t[:4]
    assert t.lilypond_format == "\\new Voice {\n\tc'16\n\td'16\n\te'16\n\tc'8 [\n\td'8\n\te'8 ]\n}"


def test_componenttools_extend_left_in_parent_of_component_06():
    '''Extend leaf leftwards of interior leaf. Do extend interior spanners.'''

    t = Voice("c'8 d'8 e'8")
    beamtools.BeamSpanner(t[:])
    result = componenttools.extend_left_in_parent_of_component(
        t[1], [Note(1.5, (1, 8))], grow_spanners=False)

    r'''
    \new Voice {
        c'8 [
        dqf'8
        d'8
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\tdqf'8\n\td'8\n\te'8 ]\n}"
    assert result == t[1:3]
