# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Spanner__is_my_first_leaf_01():
    r'''Spanner attached to flat container.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    voice = Voice(notetools.make_repeated_notes(4))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(voice)
    spanner = MockSpanner(voice)

    r'''
    \new Voice {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''

    assert spanner._is_my_first_leaf(voice[0])
    for leaf in voice[1:]:
        assert not spanner._is_my_first_leaf(leaf)
    assert spanner._is_my_last_leaf(voice[-1])
    for leaf in voice[:-1]:
        assert not spanner._is_my_last_leaf(leaf)
    for leaf in voice:
        assert not spanner._is_my_only_leaf(leaf)


def test_Spanner__is_my_first_leaf_02():
    r'''Spanner attached to container with nested contents.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(2, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(voice)
    spanner = MockSpanner(voice[:3])

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

    assert spanner._is_my_first_leaf(voice[0])
    assert spanner._is_my_last_leaf(voice[2][1])

# NONSTRUCTURAL in new parallel --> context model
#def test_Spanner__is_my_first_leaf_03():
#   r'''Spanner attached to container with parallel nested contents.'''
#
#   t = Voice(notetools.make_repeated_notes(4))
#   t.insert(2, Container(Container(notetools.make_repeated_notes(2)) * 2))
#   t[2].is_simultaneous = True
#   pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)
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
#   assert py.test.raises(ContiguityError, 'spanner = spannertools.Spanner(t[:3])')
#   #assert spanner._is_my_first_leaf(t[0])
#   #assert spanner._is_my_last_leaf(t[1])
