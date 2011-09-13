from abjad import *
import py.test


def test__NavigationInterface_first_leaves_01( ):
    '''Return first leaf from sequential container.'''

    t = Voice("c'8 d'8 e'8 f'8")
    leaves = t._navigator._first_leaves

    assert len(leaves) == 1
    assert leaves[0] is t[0]


def test__NavigationInterface_first_leaves_02( ):
    '''Return first leaves from parallel containers.'''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    t.is_parallel = True
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    leaves = t._navigator._first_leaves

    r'''
    <<
        \new Voice {
            c'8
            d'8
        }
        \new Voice {
            e'8
            f'8
        }
    >>
    '''

    leaves = t._navigator._first_leaves

    assert len(leaves) == 2
    assert leaves[0] is t[0][0]
    assert leaves[1] is t[1][0]


def test__NavigationInterface_first_leaves_03( ):
    '''Return first leaves from empty sequential container.'''

    t = Voice([ ])
    leaves = t._navigator._first_leaves
    assert len(leaves) == 0


def test__NavigationInterface_first_leaves_04( ):
    '''Return first leaves from empty parallel containes.'''

    t = Container(Voice([ ]) * 2)
    t.is_parallel = True
    leaves = t._navigator._first_leaves
    assert len(leaves) == 0
