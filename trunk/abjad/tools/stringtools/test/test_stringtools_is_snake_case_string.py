from abjad import *


def test_stringtools_is_snake_case_string_01():

    assert stringtools.is_snake_case_string('foo_bar_blah')
    assert stringtools.is_snake_case_string('foo_bar')
    assert stringtools.is_snake_case_string('foo')
    assert stringtools.is_snake_case_string('f')


def test_stringtools_is_snake_case_string_02():

    assert stringtools.is_snake_case_string('')


def test_stringtools_is_snake_case_string_03():

    assert not stringtools.is_snake_case_string('foo_Bar')
    assert not stringtools.is_snake_case_string('foo bar')
    assert not stringtools.is_snake_case_string('Foo_bar')
    assert not stringtools.is_snake_case_string('Foo_Bar')
