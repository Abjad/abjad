from abjad import *
import py.test


def test__NavigationInterface_last_leaves_01( ):
    '''Return last leaf from sequential container.'''

    t = Voice("c'8 d'8 e'8 f'8")
    leaves = t._navigator._last_leaves

    assert len(leaves) == 1
    assert leaves[0] is t[-1]


def test__NavigationInterface_last_leaves_02( ):
    '''Return last leaves from parallel containers.'''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    t.is_parallel = True
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    leaves = t._navigator._last_leaves

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

    leaves = t._navigator._last_leaves

    assert len(leaves) == 2
    assert leaves[0] is t[0][-1]
    assert leaves[1] is t[1][-1]


def test__NavigationInterface_last_leaves_03( ):
    '''Return last leaves from empty sequential container.'''

    t = Voice([ ])
    leaves = t._navigator._last_leaves

    assert len(leaves) == 0


def test__NavigationInterface_last_leaves_04( ):
    '''Return last leaves from empty parallel containes.'''

    t = Container(Voice([ ]) * 2)
    t.is_parallel = True
    leaves = t._navigator._last_leaves

    assert len(leaves) == 0
