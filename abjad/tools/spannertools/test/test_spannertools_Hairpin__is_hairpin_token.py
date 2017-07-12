# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Hairpin__is_hairpin_token_01():

    assert abjad.Hairpin._is_hairpin_token(('', '<', ''))
    assert abjad.Hairpin._is_hairpin_token(('p', '<', ''))
    assert abjad.Hairpin._is_hairpin_token(('', '<', 'f'))
    assert abjad.Hairpin._is_hairpin_token(('p', '<', 'f'))


def test_spannertools_Hairpin__is_hairpin_token_02():

    assert not abjad.Hairpin._is_hairpin_token(())
    assert not abjad.Hairpin._is_hairpin_token(('p', 'f'))
    assert not abjad.Hairpin._is_hairpin_token(('p', '@', 'f'))
    assert not abjad.Hairpin._is_hairpin_token(('x', '<', 'y'))


def test_spannertools_Hairpin__is_hairpin_token_03():

    assert not abjad.Hairpin._is_hairpin_token(('f', '<', 'p'))
    assert not abjad.Hairpin._is_hairpin_token(('p', '>', 'f'))
    assert not abjad.Hairpin._is_hairpin_token(('p', '<', 'p'))
    assert not abjad.Hairpin._is_hairpin_token(('f', '>', 'f'))
