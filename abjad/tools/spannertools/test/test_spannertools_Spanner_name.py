# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_name_01():
    staff = Staff("c'4 d'4 e'4 f'4")
    spanner = spannertools.Spanner()
    assert spanner.name is None
    attach(spanner, staff[:])
    assert spanner.name is None


def test_spannertools_Spanner_name_02():
    staff = Staff("c'4 d'4 e'4 f'4")
    spanner = spannertools.Spanner(name='foo')
    assert spanner.name == 'foo'
    attach(spanner, staff[:])
    assert spanner.name == 'foo'


def test_spannertools_Spanner_name_03():
    staff = Staff("c'4 d'4 e'4 f'4")
    spanner = spannertools.Spanner(name='foo')
    assert spanner.name == 'foo'
    attach(spanner, staff[:], name='bar')
    assert spanner.name == 'bar'


def test_spannertools_Spanner_name_04():
    staff = Staff("c'4 d'4 e'4 f'4")
    spanner = spannertools.Spanner()
    assert spanner.name is None
    attach(spanner, staff[:], name='bar')
    assert spanner.name == 'bar'
