from abjad import *


def test_iotools_is_space_delimited_lowercase_string_01():

    assert iotools.is_space_delimited_lowercase_string('foo bar blah')
    assert iotools.is_space_delimited_lowercase_string('foo bar')
    assert iotools.is_space_delimited_lowercase_string('foo')
    assert iotools.is_space_delimited_lowercase_string('f')


def test_iotools_is_space_delimited_lowercase_string_02():

    assert iotools.is_space_delimited_lowercase_string('')
    

def test_iotools_is_space_delimited_lowercase_string_03():

    assert not iotools.is_space_delimited_lowercase_string('foo_bar')
    assert not iotools.is_space_delimited_lowercase_string('foo_bar blah')
    assert not iotools.is_space_delimited_lowercase_string('Foo_Bar')
    assert not iotools.is_space_delimited_lowercase_string('FOO_BAR')
