from abjad import *


def test_stringtools_is_underscore_delimited_lowercase_string_01():

    assert stringtools.is_underscore_delimited_lowercase_string('foo_bar_blah')
    assert stringtools.is_underscore_delimited_lowercase_string('foo_bar')
    assert stringtools.is_underscore_delimited_lowercase_string('foo')
    assert stringtools.is_underscore_delimited_lowercase_string('f')


def test_stringtools_is_underscore_delimited_lowercase_string_02():

    assert stringtools.is_underscore_delimited_lowercase_string('')
    

def test_stringtools_is_underscore_delimited_lowercase_string_03():

    assert not stringtools.is_underscore_delimited_lowercase_string('foo_Bar')
    assert not stringtools.is_underscore_delimited_lowercase_string('foo bar')
    assert not stringtools.is_underscore_delimited_lowercase_string('Foo_bar')
    assert not stringtools.is_underscore_delimited_lowercase_string('Foo_Bar')
