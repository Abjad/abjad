from abjad import *


def test_iotools_is_underscore_delimited_lowercase_string_01():

    assert iotools.is_underscore_delimited_lowercase_string('foo_bar_blah')
    assert iotools.is_underscore_delimited_lowercase_string('foo_bar')
    assert iotools.is_underscore_delimited_lowercase_string('foo')
    assert iotools.is_underscore_delimited_lowercase_string('f')


def test_iotools_is_underscore_delimited_lowercase_string_02():

    assert iotools.is_underscore_delimited_lowercase_string('')
    

def test_iotools_is_underscore_delimited_lowercase_string_03():

    assert not iotools.is_underscore_delimited_lowercase_string('foo_Bar')
    assert not iotools.is_underscore_delimited_lowercase_string('foo bar')
    assert not iotools.is_underscore_delimited_lowercase_string('Foo_bar')
    assert not iotools.is_underscore_delimited_lowercase_string('Foo_Bar')
