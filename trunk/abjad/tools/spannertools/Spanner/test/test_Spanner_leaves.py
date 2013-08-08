# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Spanner_leaves_01():
    r'''Spanner attaching to container knows about both container and
    also leaves in container.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    voice = Voice(notetools.make_repeated_notes(4))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(voice)
    spanner = MockSpanner(voice)

    assert len(spanner.components) == 1
    assert spanner.components[0] is voice
    assert len(spanner.leaves) == 4
    for i, leaf in enumerate(spanner.leaves):
        assert leaf is voice[i]
    assert spanner.get_duration() == Duration(4, 8)


def test_Spanner_leaves_02():
    r'''Spanner attaching only to leaves makes spanner.components and spanner.leaves
    hold the same references.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    voice = Voice(notetools.make_repeated_notes(4))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(voice)
    spanner = MockSpanner(voice[:])

    assert len(spanner.components) == 4
    assert len(spanner.leaves) == 4
    for i, leaf in enumerate(spanner.leaves):
        assert leaf is voice[i]
    assert spanner.get_duration() == Duration(4, 8)


def test_Spanner_leaves_03():
    r'''Spanner attaching to empty container knows about container
    and also about empty leaves.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    voice = Voice([])
    spanner = MockSpanner(voice)

    assert len(spanner.components) == 1
    assert spanner.components[0] is voice
    assert len(spanner.leaves) == 0
    assert spanner.get_duration() == Duration(0)


def test_Spanner_leaves_04():
    r'''Spanner attaching to container with multidimensional contents.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(1, Container(notetools.make_repeated_notes(2)))
    voice.insert(3, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(voice)
    spanner = MockSpanner(voice)

    r'''
    \new Voice {
        c'8
        {
            cs'8
            d'8
        }
        ef'8
        {
            e'8
            f'8
        }
        fs'8
        g'8
    }
    '''

    assert len(spanner.components) == 1
    assert len(spanner.leaves) == 8
    for i, leaf in enumerate(voice.select_leaves()):
        assert leaf is voice.select_leaves()[i]
    assert spanner.get_duration() == Duration(8, 8)


def test_Spanner_leaves_05():
    r'''Spanner spanning a mixture of containers and leaves.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(1, Container(notetools.make_repeated_notes(2)))
    voice.insert(3, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(voice)
    spanner = MockSpanner(voice[0:3])

    r'''
    \new Voice {
        c'8
        {
            cs'8
            d'8
        }
        ef'8
        {
            e'8
            f'8
        }
        fs'8
        g'8
    }
    '''

    assert len(spanner.components) == 3
    assert spanner.components[0] is voice[0]
    assert spanner.components[1] is voice[1]
    assert spanner.components[2] is voice[2]
    assert len(spanner.leaves) == 4
    for i, leaf in enumerate(spanner.leaves):
        assert leaf is voice.select_leaves()[i]
    assert spanner.get_duration() == Duration(4, 8)


def test_Spanner_leaves_06():
    r'''Spanner attaching to container with some simultaneous contents.
    Spanner absolutely does not descend into simultaneous container.
    Spanner duration does, however, account for simultaneous duration.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    staff = Staff(notetools.make_repeated_notes(4))
    staff.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    staff[2].is_simultaneous = True
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        c'8
        cs'8
        <<
            \new Voice {
                d'8
                ef'8
            }
            \new Voice {
                e'8
                f'8
            }
        >>
        fs'8
        g'8
    }
    '''

    assert py.test.raises(AssertionError, 'spanner = MockSpanner(staff)')
#   assert len(spanner.components) == 1
#   assert spanner.components[0] is staff
#   assert len(spanner.leaves) == 4
#   assert spanner.leaves[0] is staff[0]
#   assert spanner.leaves[1] is staff[1]
#   assert spanner.leaves[2] is staff[3]
#   assert spanner.leaves[3] is staff[4]
#   assert spanner.get_duration() == Duration(6, 8)


def test_Spanner_leaves_07():
    r'''Spanner attaching to mixture of simultaneous and leaf components.
    Spanner absolutely does not descend into simultaneous container.
    Spanner duration does, however, account for simultaneous duration.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    staff = Staff(notetools.make_repeated_notes(4))
    staff.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    staff[2].is_simultaneous = True
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        c'8
        cs'8
        <<
            \new Voice {
                d'8
                ef'8
            }
            \new Voice {
                e'8
                f'8
            }
        >>
        fs'8
        g'8
    }
    '''

    assert py.test.raises(AssertionError, 'spanner = MockSpanner(staff[:])')
#   for i, component in enumerate(staff[:]):
#      assert component is staff[i]
#   assert len(spanner.leaves) == 4
#   assert spanner.leaves[0] is staff[0]
#   assert spanner.leaves[1] is staff[1]
#   assert spanner.leaves[2] is staff[3]
#   assert spanner.leaves[3] is staff[4]
#   assert spanner.get_duration() == Duration(6, 8)
