from abjad import *


def test_ParentageInterface_governor_01( ):
    '''Return the last sequential container in the parentage of client
        such that the next element in the parentage of client is
        either a parallel container or None.'''

    t = Voice([Container(Voice(notetools.make_repeated_notes(2)) * 2)])
    t[0].is_parallel = True
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    t[0][0].name = 'voice 1'
    t[0][1].name = 'voice 2'

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

    assert t.leaves[0]._parentage.governor is t[0][0]
    assert t.leaves[1]._parentage.governor is t[0][0]
    assert t.leaves[2]._parentage.governor is t[0][1]
    assert t.leaves[3]._parentage.governor is t[0][1]


def test_ParentageInterface_governor_02( ):
    '''Unicorporated leaves have no governor.'''

    t = Note(0, (1, 8))
    assert t._parentage.governor is None


def test_ParentageInterface_governor_03( ):
    '''Return the last sequential container in the parentage of client
        such that the next element in the parentage of client is
        either a parallel container or None.'''

    t = Staff([Voice([Container("c'8 d'8 e'8 f'8")])])

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

    assert t.leaves[0]._parentage.governor is t
    assert t.leaves[1]._parentage.governor is t
    assert t.leaves[2]._parentage.governor is t
    assert t.leaves[3]._parentage.governor is t


def test_ParentageInterface_governor_04( ):
    '''Return the last sequential container in the parentage of client
        such that the next element in the parentage of client is
        either a parallel container or None.'''

    t = Staff([Voice([Container("c'8 d'8 e'8 f'8")])])

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

    assert t[0][0]._parentage.governor is t
    assert t[0]._parentage.governor is t
    assert t._parentage.governor is t
