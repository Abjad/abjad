# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Parentage_containment_signature_01():
    r'''An anonymous staff and its contained unvoiced leaves share the same signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    containment = staff.select_parentage().containment_signature
    for component in iterationtools.iterate_components_in_expr(staff):
        assert component.select_parentage().containment_signature == containment


def test_Parentage_containment_signature_02():
    r'''A named staff and its contained unvoiced leaves share the same signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.name = 'foo'

    containment = staff.select_parentage().containment_signature
    for component in iterationtools.iterate_components_in_expr(staff):
        assert component.select_parentage().containment_signature == containment

def test_Parentage_containment_signature_03():
    r'''Leaves inside equally named sequential voices inside a staff
    share the same signature.
    '''

    staff = Staff(Voice("c'8 d'8 e'8 f'8") * 2)
    staff[0].name = 'foo'
    staff[1].name = 'foo'

    containment = staff[0][0].select_parentage().containment_signature
    for leaf in staff.select_leaves():
        assert leaf.select_parentage().containment_signature == containment


def test_Parentage_containment_signature_04():
    r'''Return ContainmentSignature giving the root and
    first voice, staff and score in the parentage of component.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    voice[2].is_parallel = True
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    voice.override.note_head.color = 'red'

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

    signatures = [leaf.select_parentage().containment_signature 
        for leaf in voice.select_leaves()]

    assert signatures[0] == signatures[1]
    assert signatures[0] != signatures[2]
    assert signatures[0] != signatures[4]
    assert signatures[0] == signatures[6]

    assert signatures[2] == signatures[3]
    assert signatures[2] != signatures[4]


def test_Parentage_containment_signature_05():
    r'''Return ContainmentSignature giving the root and
    first voice, staff and score in parentage of component.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.name = 'foo'
    voice.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    voice[2].is_parallel = True
    voice[2][0].name = 'foo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    voice.override.note_head.color = 'red'

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

    signatures = [leaf.select_parentage().containment_signature 
        for leaf in voice.select_leaves()]

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


def test_Parentage_containment_signature_06():
    r'''Return ContainmentSignature giving the root and
    first voice, staff and score in parentage of component.
    '''

    container = Container(Staff([Voice("c'8 d'8")]) * 2)
    container[0].name = 'staff1'
    container[1].name = 'staff2'
    container[0][0].name = 'voicefoo'
    container[1][0].name = 'voicefoo'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(container)
    assert py.test.raises(AssertionError, 'spannertools.BeamSpanner(container.select_leaves())')
    spannertools.BeamSpanner(container.select_leaves()[:2])
    spannertools.BeamSpanner(container.select_leaves()[2:])

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

    signatures = [leaf.select_parentage().containment_signature 
        for leaf in container.select_leaves()]

    signatures[0] == signatures[1]
    signatures[0] != signatures[2]

    signatures[2] != signatures[2]
    signatures[2] == signatures[3]


def test_Parentage_containment_signature_07():
    r'''Return ContainmentSignature giving the root and
    first voice, staff and score in parentage of component.
    '''

    container = Container(notetools.make_repeated_notes(2))
    container[1:1] = Container(Voice(notetools.make_repeated_notes(1)) * 2) * 2
    container[1].is_parallel = True
    container[1][0].name = 'alto'
    container[1][1].name = 'soprano'
    container[2][0].name = 'alto'
    container[2][1].name = 'soprano'
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(container)

    container[1][1].override.note_head.color = 'red'
    container[2][1].override.note_head.color = 'red'

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

    signatures = [leaf.select_parentage().containment_signature 
        for leaf in container.select_leaves()]

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


def test_Parentage_containment_signature_08():
    r'''Unicorporated leaves carry different containment signatures.
    '''

    t1 = Note(0, (1, 8))
    t2 = Note(0, (1, 8))

    assert t1.select_parentage().containment_signature != \
        t2.select_parentage().containment_signature


def test_Parentage_containment_signature_09():
    r'''Components here carry the same containment signature EXCEPT FOR root.
    Component containment signatures do not compare True.
    '''

    t1 = Staff([Voice([Note(0, (1, 8))])])
    t1.name = 'staff'
    t1[0].name = 'voice'

    t2 = Staff([Voice([Note(0, (1, 8))])])
    t2.name = 'staff'
    t2[0].name = 'voice'

    t1_leaf_signature = t1.select_leaves()[0].select_parentage().containment_signature
    t2_leaf_signature = t2.select_leaves()[0].select_parentage().containment_signature
    assert t1_leaf_signature != t2_leaf_signature


def test_Parentage_containment_signature_10():
    r'''Measure and leaves must carry same thread signature.
    '''

    staff = Staff([Measure((2, 8), "c'8 d'8")] + notetools.make_repeated_notes(2))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        \time 1/4
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert staff[0].select_parentage().containment_signature == \
        staff[-1].select_parentage().containment_signature
    assert staff[0].select_parentage().containment_signature == \
        staff[0][0].select_parentage().containment_signature
    assert staff[0][0].select_parentage().containment_signature == \
        staff[-1].select_parentage().containment_signature


def test_Parentage_containment_signature_11():
    r'''Leaves inside different staves have different thread signatures,
    even when the staves have the same name.
    '''

    container = Container(Staff(notetools.make_repeated_notes(2)) * 2)
    container[0].name = container[1].name = 'staff'

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

    assert container.select_leaves()[0].select_parentage().containment_signature == \
        container.select_leaves()[1].select_parentage().containment_signature
    assert container.select_leaves()[0].select_parentage().containment_signature != \
        container.select_leaves()[2].select_parentage().containment_signature
    assert container.select_leaves()[2].select_parentage().containment_signature == \
        container.select_leaves()[3].select_parentage().containment_signature
    assert container.select_leaves()[2].select_parentage().containment_signature != \
        container.select_leaves()[0].select_parentage().containment_signature
