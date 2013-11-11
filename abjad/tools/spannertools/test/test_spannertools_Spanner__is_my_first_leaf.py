# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_spannertools_Spanner__is_my_first_leaf_01():
    r'''Spanner attached to flat container.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    container = Container("c'8 cs'8 d'8 ef'8")
    spanner = MockSpanner()
    attach(spanner, container)

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        '''
        )

    assert spanner._is_my_first_leaf(container[0])
    for leaf in container[1:]:
        assert not spanner._is_my_first_leaf(leaf)
    assert spanner._is_my_last_leaf(container[-1])
    for leaf in container[:-1]:
        assert not spanner._is_my_last_leaf(leaf)
    for leaf in container:
        assert not spanner._is_my_only_leaf(leaf)


def test_spannertools_Spanner__is_my_first_leaf_02():
    r'''Spanner attached to container with nested contents.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    container = Container(
        r'''
        c'8
        cs'8
        {
            d'8
            ef'8
        }
        e'8
        f'8
        '''
        )

    spanner = MockSpanner()
    attach(spanner, container[:3])

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
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
        )

    assert spanner._is_my_first_leaf(container[0])
    assert spanner._is_my_last_leaf(container[2][1])
