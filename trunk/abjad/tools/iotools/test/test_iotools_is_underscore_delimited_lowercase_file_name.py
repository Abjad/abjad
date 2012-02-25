from abjad import *


def test_iotools_is_underscore_delimited_lowercase_file_name_01():

    assert iotools.is_underscore_delimited_lowercase_file_name('foo_bar.blah')
    assert iotools.is_underscore_delimited_lowercase_file_name('foo.blah')
    assert iotools.is_underscore_delimited_lowercase_file_name('foo_bar')
    assert iotools.is_underscore_delimited_lowercase_file_name('foo')


def test_iotools_is_underscore_delimited_lowercase_file_name_02():

    assert iotools.is_underscore_delimited_lowercase_file_name('')


def test_iotools_is_underscore_delimited_lowercase_file_name_03():

    assert not iotools.is_underscore_delimited_lowercase_file_name('foo_bar.')
    assert not iotools.is_underscore_delimited_lowercase_file_name('Foo_bar.blah')
    assert not iotools.is_underscore_delimited_lowercase_file_name('foo_bar.Blah')
    assert not iotools.is_underscore_delimited_lowercase_file_name('Foo_bar')
