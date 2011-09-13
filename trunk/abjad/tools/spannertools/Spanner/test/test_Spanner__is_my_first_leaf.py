from abjad import *
import py.test


def test_Spanner__is_my_first_leaf_01():
    '''Spanner attached to flat container.'''

    t = Voice(notetools.make_repeated_notes(4))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.Spanner(t)

    r'''
    \new Voice {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''

    assert p._is_my_first_leaf(t[0])
    for leaf in t[1:]:
        assert not p._is_my_first_leaf(leaf)
    assert p._is_my_last_leaf(t[-1])
    for leaf in t[:-1]:
        assert not p._is_my_last_leaf(leaf)
    for leaf in t:
        assert not p._is_my_only_leaf(leaf)


def test_Spanner__is_my_first_leaf_02():
    '''Spanner attached to container with nested contents.'''

    t = Voice(notetools.make_repeated_notes(4))
    t.insert(2, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.Spanner(t[:3])

    r'''
    \new Voice {
        c'8
        cs'8
        {
            d'8
            ef'8
        }
        e'8
        f'8
    }
    '''

    assert p._is_my_first_leaf(t[0])
    assert p._is_my_last_leaf(t[2][1])

# NONSTRUCTURAL in new parallel --> context model
#def test_Spanner__is_my_first_leaf_03():
#   '''Spanner attached to container with parallel nested contents.'''
#
#   t = Voice(notetools.make_repeated_notes(4))
#   t.insert(2, Container(Container(notetools.make_repeated_notes(2)) * 2))
#   t[2].is_parallel = True
#   pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
#
#   r'''\new Voice {
#      c'8
#      cs'8
#      <<
#         {
#            d'8
#            ef'8
#         }
#         {
#            e'8
#            f'8
#         }
#      >>
#      fs'8
#      g'8
#   }'''
#
#   assert py.test.raises(ContiguityError, 'p = spannertools.Spanner(t[:3])')
#   #assert p._is_my_first_leaf(t[0])
#   #assert p._is_my_last_leaf(t[1])
