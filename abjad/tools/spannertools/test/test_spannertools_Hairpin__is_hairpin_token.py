# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin__is_hairpin_token_01():

    assert Hairpin._is_hairpin_token(('', '<', ''))
    assert Hairpin._is_hairpin_token(('p', '<', ''))
    assert Hairpin._is_hairpin_token(('', '<', 'f'))
    assert Hairpin._is_hairpin_token(('p', '<', 'f'))


def test_spannertools_Hairpin__is_hairpin_token_02():

    assert not Hairpin._is_hairpin_token(())
    assert not Hairpin._is_hairpin_token(('p', 'f'))
    assert not Hairpin._is_hairpin_token(('p', '@', 'f'))
    assert not Hairpin._is_hairpin_token(('x', '<', 'y'))


def test_spannertools_Hairpin__is_hairpin_token_03():

    assert not Hairpin._is_hairpin_token(('f', '<', 'p'))
    assert not Hairpin._is_hairpin_token(('p', '>', 'f'))
    assert not Hairpin._is_hairpin_token(('p', '<', 'p'))
    assert not Hairpin._is_hairpin_token(('f', '>', 'f'))
