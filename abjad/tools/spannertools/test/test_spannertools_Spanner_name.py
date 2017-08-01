# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Spanner_name_01():
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    spanner = abjad.Spanner()
    assert spanner.name is None
    abjad.attach(spanner, staff[:])
    assert spanner.name is None


def test_spannertools_Spanner_name_02():
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    spanner = abjad.Spanner(name='foo')
    assert spanner.name == 'foo'
    abjad.attach(spanner, staff[:])
    assert spanner.name == 'foo'
