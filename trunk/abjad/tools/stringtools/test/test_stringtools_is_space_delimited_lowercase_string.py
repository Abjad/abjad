from abjad import *


def test_stringtools_is_space_delimited_lowercase_string_01():

    assert stringtools.is_space_delimited_lowercase_string('foo bar blah')
    assert stringtools.is_space_delimited_lowercase_string('foo bar')
    assert stringtools.is_space_delimited_lowercase_string('foo')
    assert stringtools.is_space_delimited_lowercase_string('f')


def test_stringtools_is_space_delimited_lowercase_string_02():

    assert stringtools.is_space_delimited_lowercase_string('')
    

def test_stringtools_is_space_delimited_lowercase_string_03():

    assert not stringtools.is_space_delimited_lowercase_string('foo_bar')
    assert not stringtools.is_space_delimited_lowercase_string('foo_bar blah')
    assert not stringtools.is_space_delimited_lowercase_string('Foo_Bar')
    assert not stringtools.is_space_delimited_lowercase_string('FOO_BAR')
