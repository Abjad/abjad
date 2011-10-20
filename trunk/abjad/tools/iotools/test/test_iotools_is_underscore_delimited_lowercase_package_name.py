from abjad import *


def test_iotools_is_underscore_delimited_lowercase_package_name_01():

    assert iotools.is_underscore_delimited_lowercase_package_name('foo.bar.blah')
    assert iotools.is_underscore_delimited_lowercase_package_name('foo.bar_blah')
    assert iotools.is_underscore_delimited_lowercase_package_name('foo_bar.blah')
    assert iotools.is_underscore_delimited_lowercase_package_name('foo')


def test_iotools_is_underscore_delimited_lowercase_package_name_02():

    assert iotools.is_underscore_delimited_lowercase_package_name('')
    

def test_iotools_is_underscore_delimited_lowercase_package_name_03():

    assert not iotools.is_underscore_delimited_lowercase_package_name('foo.bar.Blah')
    assert not iotools.is_underscore_delimited_lowercase_package_name('foo.bar.BlahPackage')
    assert not iotools.is_underscore_delimited_lowercase_package_name('Foo')
    assert not iotools.is_underscore_delimited_lowercase_package_name('Foo.Bar')
