# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_selectiontools_Parentage_logical_voice_01():
    r'''An anonymous staff and its contained unvoiced leaves share
    the same signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    containment = inspect_(staff).get_parentage().logical_voice
    for component in iterate(staff).by_class():
        assert inspect_(component).get_parentage().logical_voice == containment


def test_selectiontools_Parentage_logical_voice_02():
    r'''A named staff and its contained unvoiced leaves share
    the same signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.name = 'foo'

    containment = inspect_(staff).get_parentage().logical_voice
    for component in iterate(staff).by_class():
        assert inspect_(component).get_parentage().logical_voice == containment

def test_selectiontools_Parentage_logical_voice_03():
    r'''Leaves inside equally named sequential voices inside a staff
    share the same signature.
    '''

    staff = Staff(Voice("c'8 d'8 e'8 f'8") * 2)
    staff[0].name = 'foo'
    staff[1].name = 'foo'

    containment = inspect_(staff[0][0]).get_parentage().logical_voice
    for leaf in staff.select_leaves():
        assert inspect_(leaf).get_parentage().logical_voice == containment


def test_selectiontools_Parentage_logical_voice_04():
    r'''Returns logical voice giving the root and
    first voice, staff and score in the parentage of component.
    '''

    voice = Voice(
        r'''
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
        '''
        )

    override(voice).note_head.color = 'red'

    assert systemtools.TestManager.compare(
        voice,
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
        )

    signatures = [inspect_(leaf).get_parentage().logical_voice
        for leaf in voice.select_leaves(allow_discontiguous_leaves=True)]

    assert signatures[0] == signatures[1]
    assert signatures[0] != signatures[2]
    assert signatures[0] != signatures[4]
    assert signatures[0] == signatures[6]

    assert signatures[2] == signatures[3]
    assert signatures[2] != signatures[4]


def test_selectiontools_Parentage_logical_voice_05():
    r'''Returns logical voice giving the root and
    first voice, staff and score in parentage of component.
    '''

    voice = Voice(
        r'''
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
        '''
        )

    override(voice).note_head.color = 'red'
    voice.name = 'foo'

    assert systemtools.TestManager.compare(
        voice,
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
        )

    signatures = [inspect_(leaf).get_parentage().logical_voice
        for leaf in voice.select_leaves(allow_discontiguous_leaves=True)]

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


def test_selectiontools_Parentage_logical_voice_06():
    r'''Returns logical voice giving the root and
    first voice, staff and score in parentage of component.
    '''

    container = Container([
        Staff([Voice("c'8 d'8")]),
        Staff([Voice("e'8 f'8")]),
        ])
    container[0].name = 'staff1'
    container[1].name = 'staff2'
    container[0][0].name = 'voicefoo'
    container[1][0].name = 'voicefoo'
    beam = Beam()
    statement = 'attach(beam, container.select_leaves())'
    assert pytest.raises(AssertionError, statement)
    leaves = container.select_leaves(allow_discontiguous_leaves=True)
    beam = Beam()
    attach(beam, leaves[:2])
    beam = Beam()
    attach(beam, leaves[2:])

    assert systemtools.TestManager.compare(
        container,
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
        )

    signatures = [inspect_(leaf).get_parentage().logical_voice
        for leaf in leaves]

    signatures[0] == signatures[1]
    signatures[0] != signatures[2]

    signatures[2] != signatures[2]
    signatures[2] == signatures[3]


def test_selectiontools_Parentage_logical_voice_07():
    r'''Returns logical voice giving the root and
    first voice, staff and score in parentage of component.
    '''

    container = Container(
        r'''
        c'8
        <<
            \context Voice = "alto" {
                d'8
            }
            \context Voice = "soprano" {
                e'8
            }
        >>
        {
            \context Voice = "alto" {
                f'8
            }
            \context Voice = "soprano" {
                g'8
            }
        }
        a'8
        '''
        )

    override(container[1][1]).note_head.color = 'red'
    override(container[2][1]).note_head.color = 'red'

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8
            <<
                \context Voice = "alto" {
                    d'8
                }
                \context Voice = "soprano" \with {
                    \override NoteHead #'color = #red
                } {
                    e'8
                }
            >>
            {
                \context Voice = "alto" {
                    f'8
                }
                \context Voice = "soprano" \with {
                    \override NoteHead #'color = #red
                } {
                    g'8
                }
            }
            a'8
        }
        '''
        )

    signatures = [inspect_(leaf).get_parentage().logical_voice
        for leaf in container.select_leaves(allow_discontiguous_leaves=True)]

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


def test_selectiontools_Parentage_logical_voice_08():
    r'''Unicorporated leaves carry equivalent containment signatures.
    '''

    note_1 = Note(0, (1, 8))
    note_2 = Note(0, (1, 8))

    signature_1 = inspect_(note_1).get_parentage().logical_voice
    signature_2 = inspect_(note_2).get_parentage().logical_voice
    assert signature_1 == signature_2


def test_selectiontools_Parentage_logical_voice_09():
    r'''Notes appear in the same logical voice.
    '''

    t1 = Staff([Voice([Note(0, (1, 8))])])
    t1.name = 'staff'
    t1[0].name = 'voice'

    t2 = Staff([Voice([Note(0, (1, 8))])])
    t2.name = 'staff'
    t2[0].name = 'voice'

    t1_leaf_signature = inspect_(t1.select_leaves()[0]).get_parentage().logical_voice
    t2_leaf_signature = inspect_(t2.select_leaves()[0]).get_parentage().logical_voice
    assert t1_leaf_signature == t2_leaf_signature


def test_selectiontools_Parentage_logical_voice_10():
    r'''Measure and leaves must carry same logical voice signature.
    '''

    staff = Staff(r'''
        {
            \time 2/8
            c'8
            d'8
        }
        e'8
        f'8
        ''')

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            e'8
            f'8
        }
        '''
        )

    assert inspect_(staff[0]).get_parentage().logical_voice == \
        inspect_(staff[-1]).get_parentage().logical_voice
    assert inspect_(staff[0]).get_parentage().logical_voice == \
        inspect_(staff[0][0]).get_parentage().logical_voice
    assert inspect_(staff[0][0]).get_parentage().logical_voice == \
        inspect_(staff[-1]).get_parentage().logical_voice


def test_selectiontools_Parentage_logical_voice_11():
    r'''Leaves inside different staves have different logical voice
    signatures, even when the staves have the same name.
    '''

    container = Container(2 * Staff("c'8 c'8"))
    container[0].name = container[1].name = 'staff'

    assert systemtools.TestManager.compare(
        container,
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
        )

    leaves = container.select_leaves(allow_discontiguous_leaves=True)
    assert inspect_(leaves[0]).get_parentage().logical_voice == \
        inspect_(leaves[1]).get_parentage().logical_voice
    assert inspect_(leaves[0]).get_parentage().logical_voice != \
        inspect_(leaves[2]).get_parentage().logical_voice
    assert inspect_(leaves[2]).get_parentage().logical_voice == \
        inspect_(leaves[3]).get_parentage().logical_voice
    assert inspect_(leaves[2]).get_parentage().logical_voice != \
        inspect_(leaves[0]).get_parentage().logical_voice