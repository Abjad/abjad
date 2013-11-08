# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin_is_hairpin_token_01():

    assert Hairpin.is_hairpin_token(('', '<', ''))
    assert Hairpin.is_hairpin_token(('p', '<', ''))
    assert Hairpin.is_hairpin_token(('', '<', 'f'))
    assert Hairpin.is_hairpin_token(('p', '<', 'f'))


def test_spannertools_Hairpin_is_hairpin_token_02():

    assert not Hairpin.is_hairpin_token(())
    assert not Hairpin.is_hairpin_token(('p', 'f'))
    assert not Hairpin.is_hairpin_token(('p', '@', 'f'))
    assert not Hairpin.is_hairpin_token(('x', '<', 'y'))


def test_spannertools_Hairpin_is_hairpin_token_03():

    assert not Hairpin.is_hairpin_token(('f', '<', 'p'))
    assert not Hairpin.is_hairpin_token(('p', '>', 'f'))
    assert not Hairpin.is_hairpin_token(('p', '<', 'p'))
    assert not Hairpin.is_hairpin_token(('f', '>', 'f'))
