# -*- coding: utf-8 -*-
from abjad import *


def test_stringtools_is_space_delimited_lowercase_01():

    assert stringtools.is_space_delimited_lowercase('foo bar blah')
    assert stringtools.is_space_delimited_lowercase('foo bar')
    assert stringtools.is_space_delimited_lowercase('foo')
    assert stringtools.is_space_delimited_lowercase('f')


def test_stringtools_is_space_delimited_lowercase_02():

    assert stringtools.is_space_delimited_lowercase('')


def test_stringtools_is_space_delimited_lowercase_03():

    assert not stringtools.is_space_delimited_lowercase('foo_bar')
    assert not stringtools.is_space_delimited_lowercase('foo_bar blah')
    assert not stringtools.is_space_delimited_lowercase('Foo_Bar')
    assert not stringtools.is_space_delimited_lowercase('FOO_BAR')
