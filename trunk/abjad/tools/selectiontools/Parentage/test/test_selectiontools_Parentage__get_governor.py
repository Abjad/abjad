# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_Parentage__get_governor_01( ):
    r'''Returns the last sequential container in the parentage of client
    such that the next element in the parentage of client is
    either a simultaneous container or None.
    '''

    voice = Voice([Container([Voice("c'8 d'8"), Voice("e'8 f'8")])])
    voice[0].is_simultaneous = True
    voice[0][0].name = 'voice 1'
    voice[0][1].name = 'voice 2'

    r'''
    \new Voice {
        <<
            \context Voice = "voice 1" {
                c'8
                d'8
            }
            \context Voice = "voice 2" {
                e'8
                f'8
            }
        >>
    }
    '''

    assert inspect(voice.select_leaves(allow_discontiguous_leaves=True)[0]).get_parentage()._get_governor() is voice[0][0]
    assert inspect(voice.select_leaves(allow_discontiguous_leaves=True)[1]).get_parentage()._get_governor() is voice[0][0]
    assert inspect(voice.select_leaves(allow_discontiguous_leaves=True)[2]).get_parentage()._get_governor() is voice[0][1]
    assert inspect(voice.select_leaves(allow_discontiguous_leaves=True)[3]).get_parentage()._get_governor() is voice[0][1]


def test_selectiontools_Parentage__get_governor_02( ):
    r'''Unicorporated leaves have no governor.
    '''

    note = Note(0, (1, 8))
    assert inspect(note).get_parentage()._get_governor() is None


def test_selectiontools_Parentage__get_governor_03( ):
    r'''Returns the last sequential container in the parentage of client
        such that the next element in the parentage of client is
        either a simultaneous container or None.'''

    staff = Staff([Voice([Container("c'8 d'8 e'8 f'8")])])

    r'''
    \new Staff {
        \new Voice {
            {
                c'8
                d'8
                e'8
                f'8
            }
        }
    }
    '''

    assert inspect(staff.select_leaves(allow_discontiguous_leaves=True)[0]).get_parentage()._get_governor() is staff
    assert inspect(staff.select_leaves(allow_discontiguous_leaves=True)[1]).get_parentage()._get_governor() is staff
    assert inspect(staff.select_leaves(allow_discontiguous_leaves=True)[2]).get_parentage()._get_governor() is staff
    assert inspect(staff.select_leaves(allow_discontiguous_leaves=True)[3]).get_parentage()._get_governor() is staff


def test_selectiontools_Parentage__get_governor_04( ):
    r'''Returns the last sequential container in the parentage of client
    such that the next element in the parentage of client is
    either a simultaneous container or None.
    '''

    staff = Staff([Voice([Container("c'8 d'8 e'8 f'8")])])

    r'''
    \new Staff {
        \new Voice {
            {
                c'8
                d'8
                e'8
                f'8
            }
        }
    }
    '''

    assert inspect(staff[0][0]).get_parentage()._get_governor() is staff
    assert inspect(staff[0]).get_parentage()._get_governor() is staff
    assert inspect(staff).get_parentage()._get_governor() is staff
