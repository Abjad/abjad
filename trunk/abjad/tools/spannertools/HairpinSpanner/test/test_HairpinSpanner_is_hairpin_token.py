from abjad import *


def test_HairpinSpanner_is_hairpin_token_01():

    assert spannertools.HairpinSpanner.is_hairpin_token(('', '<', ''))
    assert spannertools.HairpinSpanner.is_hairpin_token(('p', '<', ''))
    assert spannertools.HairpinSpanner.is_hairpin_token(('', '<', 'f'))
    assert spannertools.HairpinSpanner.is_hairpin_token(('p', '<', 'f'))


def test_HairpinSpanner_is_hairpin_token_02():

    assert not spannertools.HairpinSpanner.is_hairpin_token(())
    assert not spannertools.HairpinSpanner.is_hairpin_token(('p', 'f'))
    assert not spannertools.HairpinSpanner.is_hairpin_token(('p', '@', 'f'))
    assert not spannertools.HairpinSpanner.is_hairpin_token(('x', '<', 'y'))


def test_HairpinSpanner_is_hairpin_token_03():

    assert not spannertools.HairpinSpanner.is_hairpin_token(('f', '<', 'p'))
    assert not spannertools.HairpinSpanner.is_hairpin_token(('p', '>', 'f'))
    assert not spannertools.HairpinSpanner.is_hairpin_token(('p', '<', 'p'))
    assert not spannertools.HairpinSpanner.is_hairpin_token(('f', '>', 'f'))
