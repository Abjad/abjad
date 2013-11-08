# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_HairpinSpanner_is_hairpin_token_01():

    assert HairpinSpanner.is_hairpin_token(('', '<', ''))
    assert HairpinSpanner.is_hairpin_token(('p', '<', ''))
    assert HairpinSpanner.is_hairpin_token(('', '<', 'f'))
    assert HairpinSpanner.is_hairpin_token(('p', '<', 'f'))


def test_spannertools_HairpinSpanner_is_hairpin_token_02():

    assert not HairpinSpanner.is_hairpin_token(())
    assert not HairpinSpanner.is_hairpin_token(('p', 'f'))
    assert not HairpinSpanner.is_hairpin_token(('p', '@', 'f'))
    assert not HairpinSpanner.is_hairpin_token(('x', '<', 'y'))


def test_spannertools_HairpinSpanner_is_hairpin_token_03():

    assert not HairpinSpanner.is_hairpin_token(('f', '<', 'p'))
    assert not HairpinSpanner.is_hairpin_token(('p', '>', 'f'))
    assert not HairpinSpanner.is_hairpin_token(('p', '<', 'p'))
    assert not HairpinSpanner.is_hairpin_token(('f', '>', 'f'))
