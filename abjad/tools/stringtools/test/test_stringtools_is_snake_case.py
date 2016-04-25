# -*- coding: utf-8 -*-
from abjad import *


def test_stringtools_is_snake_case_01():

    assert stringtools.is_snake_case('foo_bar_blah')
    assert stringtools.is_snake_case('foo_bar')
    assert stringtools.is_snake_case('foo')
    assert stringtools.is_snake_case('f')


def test_stringtools_is_snake_case_02():

    assert stringtools.is_snake_case('')


def test_stringtools_is_snake_case_03():

    assert not stringtools.is_snake_case('foo_Bar')
    assert not stringtools.is_snake_case('foo bar')
    assert not stringtools.is_snake_case('Foo_bar')
    assert not stringtools.is_snake_case('Foo_Bar')
