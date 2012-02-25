from abjad import *


def test_iotools_is_underscore_delimited_lowercase_file_name_with_extension_01():

    assert iotools.is_underscore_delimited_lowercase_file_name_with_extension('foo_bar.blah')
    assert iotools.is_underscore_delimited_lowercase_file_name_with_extension('foo.blah')


def test_iotools_is_underscore_delimited_lowercase_file_name_with_extension_02():

    assert iotools.is_underscore_delimited_lowercase_file_name_with_extension('')


def test_iotools_is_underscore_delimited_lowercase_file_name_with_extension_03():

    assert not iotools.is_underscore_delimited_lowercase_file_name_with_extension('foo_bar')
    assert not iotools.is_underscore_delimited_lowercase_file_name_with_extension('foo_bar.')
    assert not iotools.is_underscore_delimited_lowercase_file_name_with_extension('Foo_bar.blah')
    assert not iotools.is_underscore_delimited_lowercase_file_name_with_extension('foo_bar.Blah')
