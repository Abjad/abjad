from abjad import *
import py.test


def test_componenttools_component_to_containment_signature_01():
    '''An anonymous  Staff and it's contained unvoiced leaves share the same signature.
    '''

    t = Staff("c'8 d'8 e'8 f'8")

    containment = componenttools.component_to_containment_signature(t)
    for component in iterationtools.iterate_components_in_expr(t):
        assert componenttools.component_to_containment_signature(component) == containment


def test_componenttools_component_to_containment_signature_02():
    '''A named Staff and it's contained unvoiced leaves share the same signature.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.name = 'foo'

    containment = componenttools.component_to_containment_signature(t)
    for component in iterationtools.iterate_components_in_expr(t):
        assert componenttools.component_to_containment_signature(component) == containment

def test_componenttools_component_to_containment_signature_03():
    '''Leaves inside equally named sequential voices inside a Staff
    share the same signature.
    '''

    t = Staff(Voice("c'8 d'8 e'8 f'8") * 2)
    t[0].name = 'foo'
    t[1].name = 'foo'

    containment = componenttools.component_to_containment_signature(t[0][0])
    for leaf in t.leaves:
        assert componenttools.component_to_containment_signature(leaf) == containment


def test_componenttools_component_to_containment_signature_04():
    '''Return ContainmentSignature giving the root and
    first voice, staff and score in the parentage of component.
    '''

    t = Voice(notetools.make_repeated_notes(4))
    t.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    t[2].is_parallel = True
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    t.override.note_head.color = 'red'

    r'''
    \new Voice \with {
        \override NoteHead #'color = #red
    } {
        c'8
        d'8
        <<
            \new Voice {
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
            }
        >>
        b'8
        c''8
    }
    '''

    signatures = [componenttools.component_to_containment_signature(leaf) for leaf in t.leaves]

    assert signatures[0] == signatures[1]
    assert signatures[0] != signatures[2]
    assert signatures[0] != signatures[4]
    assert signatures[0] == signatures[6]

    assert signatures[2] == signatures[3]
    assert signatures[2] != signatures[4]


def test_componenttools_component_to_containment_signature_05():
    '''Return ContainmentSignature giving the root and
    first voice, staff and score in parentage of component.
    '''

    t = Voice(notetools.make_repeated_notes(4))
    t.name = 'foo'
    t.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    t[2].is_parallel = True
    t[2][0].name = 'foo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    t.override.note_head.color = 'red'

    r'''
    \context Voice = "foo" \with {
        \override NoteHead #'color = #red
    } {
        c'8
        d'8
        <<
            \context Voice = "foo" {
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
            }
        >>
        b'8
        c''8
    }
    '''

    signatures = [componenttools.component_to_containment_signature(leaf) for leaf in t.leaves]

    signatures[0] == signatures[1]
    signatures[0] == signatures[2]
    signatures[0] != signatures[4]
    signatures[0] == signatures[6]

    signatures[2] == signatures[0]
    signatures[2] == signatures[3]
    signatures[2] == signatures[4]
    signatures[2] == signatures[6]

    signatures[4] != signatures[0]
    signatures[4] != signatures[2]
    signatures[4] == signatures[5]
    signatures[4] == signatures[6]


def test_componenttools_component_to_containment_signature_06():
    '''Return ContainmentSignature giving the root and
    first voice, staff and score in parentage of component.
    '''

    t = Container(Staff([Voice("c'8 d'8")]) * 2)
    t[0].name = 'staff1'
    t[1].name = 'staff2'
    t[0][0].name = 'voicefoo'
    t[1][0].name = 'voicefoo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    assert py.test.raises(AssertionError, 'beamtools.BeamSpanner(t.leaves)')
    beamtools.BeamSpanner(t.leaves[:2])
    beamtools.BeamSpanner(t.leaves[2:])

    r'''
    {
        \context Staff = "staff1" {
            \context Voice = "voicefoo" {
                c'8 [
                d'8 ]
            }
        }
        \context Staff = "staff2" {
            \context Voice = "voicefoo" {
                e'8 [
                f'8 ]
            }
        }
    }
    '''

    signatures = [componenttools.component_to_containment_signature(leaf) for leaf in t.leaves]

    signatures[0] == signatures[1]
    signatures[0] != signatures[2]

    signatures[2] != signatures[2]
    signatures[2] == signatures[3]


def test_componenttools_component_to_containment_signature_07():
    '''Return ContainmentSignature giving the root and
    first voice, staff and score in parentage of component.
    '''

    t = Container(notetools.make_repeated_notes(2))
    t[1:1] = Container(Voice(notetools.make_repeated_notes(1)) * 2) * 2
    t[1].is_parallel = True
    t[1][0].name = 'alto'
    t[1][1].name = 'soprano'
    t[2][0].name = 'alto'
    t[2][1].name = 'soprano'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    t[1][1].override.note_head.color = 'red'
    t[2][1].override.note_head.color = 'red'

    r'''
    {
        c'8
        <<
            \context Voice = "alto" {
                d'8
            }
            \context Voice = "soprano" {
                \override NoteHead #'color = #red
                e'8
            }
        >>
        <<
            \context Voice = "alto" {
                f'8
            }
            \context Voice = "soprano" {
                g'8
                \revert NoteHead #'color
            }
        >>
        a'8
    }
    '''

    signatures = [componenttools.component_to_containment_signature(leaf) for leaf in t.leaves]

    signatures[0] != signatures[1]
    signatures[0] != signatures[2]
    signatures[0] != signatures[3]
    signatures[0] != signatures[4]
    signatures[0] == signatures[5]

    signatures[1] != signatures[0]
    signatures[1] != signatures[2]
    signatures[1] == signatures[3]
    signatures[1] != signatures[4]
    signatures[1] != signatures[5]

    signatures[2] != signatures[0]
    signatures[2] != signatures[1]
    signatures[2] != signatures[3]
    signatures[2] == signatures[4]
    signatures[2] != signatures[5]


def test_componenttools_component_to_containment_signature_08():
    '''Unicorporated leaves carry different containment signatures.'''

    t1 = Note(0, (1, 8))
    t2 = Note(0, (1, 8))

    assert componenttools.component_to_containment_signature(t1) != \
        componenttools.component_to_containment_signature(t2)


def test_componenttools_component_to_containment_signature_09():
    '''Components here carry the same containment signature EXCEPT FOR root.
    Component containment signatures do not compare True.
    '''

    t1 = Staff([Voice([Note(0, (1, 8))])])
    t1.name = 'staff'
    t1[0].name = 'voice'

    t2 = Staff([Voice([Note(0, (1, 8))])])
    t2.name = 'staff'
    t2[0].name = 'voice'

    t1_leaf_signature = componenttools.component_to_containment_signature(t1.leaves[0])
    t2_leaf_signature = componenttools.component_to_containment_signature(t2.leaves[0])
    assert t1_leaf_signature != t2_leaf_signature


def test_componenttools_component_to_containment_signature_10():
    '''Measure and leaves must carry same thread signature.
    '''

    t = Staff([measuretools.DynamicMeasure("c'8 d'8")] + notetools.make_repeated_notes(2))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        \time 1/4
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.component_to_containment_signature(t[0]) == \
        componenttools.component_to_containment_signature(t[-1])
    assert componenttools.component_to_containment_signature(t[0]) == \
        componenttools.component_to_containment_signature(t[0][0])
    assert componenttools.component_to_containment_signature(t[0][0]) == \
        componenttools.component_to_containment_signature(t[-1])


def test_componenttools_component_to_containment_signature_11():
    '''Leaves inside different staves have different thread signatures,
    even when the staves have the same name.
    '''

    t = Container(Staff(notetools.make_repeated_notes(2)) * 2)
    t[0].name = t[1].name = 'staff'

    r'''
    {
        \context Staff = "staff" {
            c'8
            c'8
        }
        \context Staff = "staff" {
            c'8
            c'8
        }
    }
    '''

    assert componenttools.component_to_containment_signature(t.leaves[0]) == \
        componenttools.component_to_containment_signature(t.leaves[1])
    assert componenttools.component_to_containment_signature(t.leaves[0]) != \
        componenttools.component_to_containment_signature(t.leaves[2])
    assert componenttools.component_to_containment_signature(t.leaves[2]) == \
        componenttools.component_to_containment_signature(t.leaves[3])
    assert componenttools.component_to_containment_signature(t.leaves[2]) != \
        componenttools.component_to_containment_signature(t.leaves[0])
