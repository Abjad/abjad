# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Parentage_parentage_signature_01():
    r'''An anonymous staff and its contained unvoiced leaves share the
    same parentage signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    containment = more(staff).select_parentage().parentage_signature
    for component in iterationtools.iterate_components_in_expr(staff):
        assert more(component).select_parentage().parentage_signature == containment


def test_Parentage_parentage_signature_02():
    r'''A named staff and its contained unvoiced leaves share the
    same parentage signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.name = 'foo'

    containment = more(staff).select_parentage().parentage_signature
    for component in iterationtools.iterate_components_in_expr(staff):
        assert more(component).select_parentage().parentage_signature == containment


def test_Parentage_parentage_signature_03():
    r'''Leaves inside equally named sequential voices inside a Staff
    share the same parentage signature.
    '''

    staff = Staff(Voice("c'8 d'8 e'8 f'8") * 2)
    staff[0].name = 'foo'
    staff[1].name = 'foo'

    containment = more(staff[0][0]).select_parentage().parentage_signature
    for leaf in staff.select_leaves():
        assert more(leaf).select_parentage().parentage_signature == containment


def test_Parentage_parentage_signature_04():
    r'''Return ContainmentSignature giving the root and
    first voice, staff and score in the parentage of component.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    voice[2].is_simultaneous = True
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

    signatures = [more(leaf).select_parentage().parentage_signature 
        for leaf in voice.select_leaves(allow_discontiguous_leaves=True)]

    assert signatures[0] == signatures[1]
    assert signatures[0] != signatures[2]
    assert signatures[0] != signatures[4]
    assert signatures[0] == signatures[6]

    assert signatures[2] == signatures[3]
    assert signatures[2] != signatures[4]


def test_Parentage_parentage_signature_05():
    r'''Unicorporated leaves carry different parentage signatures.
    '''

    t1 = Note(0, (1, 8))
    t2 = Note(0, (1, 8))

    assert more(t1).select_parentage().parentage_signature != \
        more(t2).select_parentage().parentage_signature


def test_Parentage_parentage_signature_06():
    r'''Leaves inside different Staves with the same name have the same
    parentage signature.
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

    leaves = container.select_leaves(allow_discontiguous_leaves=True)
    assert more(leaves[0]).select_parentage().parentage_signature == \
        more(leaves[1]).select_parentage().parentage_signature
    assert more(leaves[0]).select_parentage().parentage_signature == \
        more(leaves[2]).select_parentage().parentage_signature
    assert more(leaves[2]).select_parentage().parentage_signature == \
        more(leaves[3]).select_parentage().parentage_signature
    assert more(leaves[2]).select_parentage().parentage_signature == \
        more(leaves[0]).select_parentage().parentage_signature

    assert more(leaves[0]).select_parentage().parentage_signature == \
        more(leaves[1]).select_parentage().parentage_signature
