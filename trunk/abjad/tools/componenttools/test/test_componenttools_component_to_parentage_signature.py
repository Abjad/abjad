from abjad import *
import py.test


def test_componenttools_component_to_parentage_signature_01():
    '''An anonymous Staff and it's contained unvoiced leaves share the
    same parentage signature.'''

    t = Staff("c'8 d'8 e'8 f'8")

    containment = componenttools.component_to_parentage_signature(t)
    for component in componenttools.iterate_components_forward_in_expr(t):
        assert componenttools.component_to_parentage_signature(component) == containment


def test_componenttools_component_to_parentage_signature_02():
    '''A named Staff and it's contained unvoiced leaves share the
    same parentage signature.'''

    t = Staff("c'8 d'8 e'8 f'8")
    t.name = 'foo'

    containment = componenttools.component_to_parentage_signature(t)
    for component in componenttools.iterate_components_forward_in_expr(t):
        assert componenttools.component_to_parentage_signature(component) == containment


def test_componenttools_component_to_parentage_signature_03():
    '''Leaves inside equally named sequential voices inside a Staff
    share the same parentage signature.'''

    t = Staff(Voice("c'8 d'8 e'8 f'8") * 2)
    t[0].name = 'foo'
    t[1].name = 'foo'

    containment = componenttools.component_to_parentage_signature(t[0][0])
    for leaf in t.leaves:
        assert componenttools.component_to_parentage_signature(leaf) == containment


def test_componenttools_component_to_parentage_signature_04():
    '''Return _ContainmentSignature giving the root and
        first voice, staff and score in the parentage of component.'''

    t = Voice(notetools.make_repeated_notes(4))
    t.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    t[2].is_parallel = True
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
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

    signatures = [componenttools.component_to_parentage_signature(leaf) for leaf in t.leaves]

    assert signatures[0] == signatures[1]
    assert signatures[0] != signatures[2]
    assert signatures[0] != signatures[4]
    assert signatures[0] == signatures[6]

    assert signatures[2] == signatures[3]
    assert signatures[2] != signatures[4]


def test_componenttools_component_to_parentage_signature_05():
    '''Unicorporated leaves carry different parentage signatures.'''

    t1 = Note(0, (1, 8))
    t2 = Note(0, (1, 8))

    assert componenttools.component_to_parentage_signature(t1) != \
        componenttools.component_to_parentage_signature(t2)


def test_componenttools_component_to_parentage_signature_06():
    '''Leaves inside different Staves with the same name have the same
    parentage signature.'''

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

    assert componenttools.component_to_parentage_signature(t.leaves[0]) == \
        componenttools.component_to_parentage_signature(t.leaves[1])
    assert componenttools.component_to_parentage_signature(t.leaves[0]) == \
        componenttools.component_to_parentage_signature(t.leaves[2])
    assert componenttools.component_to_parentage_signature(t.leaves[2]) == \
        componenttools.component_to_parentage_signature(t.leaves[3])
    assert componenttools.component_to_parentage_signature(t.leaves[2]) == \
        componenttools.component_to_parentage_signature(t.leaves[0])

    assert componenttools.component_to_parentage_signature(t[0]) == \
        componenttools.component_to_parentage_signature(t[1])
