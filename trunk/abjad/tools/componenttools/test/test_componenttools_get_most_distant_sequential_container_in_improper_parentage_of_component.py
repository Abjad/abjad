from abjad import *


def test_componenttools_get_most_distant_sequential_container_in_improper_parentage_of_component_01( ):
    '''Return the last sequential container in the parentage of client
    such that the next element in the parentage of client is
    either a parallel container or None.
    '''

    t = Voice([Container(Voice(notetools.make_repeated_notes(2)) * 2)])
    t[0].is_parallel = True
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
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

    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t.leaves[0]) is t[0][0]
    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t.leaves[1]) is t[0][0]
    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t.leaves[2]) is t[0][1]
    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t.leaves[3]) is t[0][1]


def test_componenttools_get_most_distant_sequential_container_in_improper_parentage_of_component_02( ):
    '''Unicorporated leaves have no governor.'''

    t = Note(0, (1, 8))
    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(t) is None


def test_componenttools_get_most_distant_sequential_container_in_improper_parentage_of_component_03( ):
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

    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t.leaves[0]) is t
    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t.leaves[1]) is t
    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t.leaves[2]) is t
    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t.leaves[3]) is t


def test_componenttools_get_most_distant_sequential_container_in_improper_parentage_of_component_04( ):
    '''Return the last sequential container in the parentage of client
    such that the next element in the parentage of client is
    either a parallel container or None.
    '''

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

    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t[0][0]) is t
    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t[0]) is t
    assert componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        t) is t
