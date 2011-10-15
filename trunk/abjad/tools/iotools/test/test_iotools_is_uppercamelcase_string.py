from abjad import *


def test_iotools_is_uppercamelcase_string_01():

    assert iotools.is_uppercamelcase_string('FooBar')
    assert iotools.is_uppercamelcase_string('Foo')
    assert iotools.is_uppercamelcase_string('FB')
    assert iotools.is_uppercamelcase_string('F')


def test_iotools_is_uppercamelcase_string_02():

    assert iotools.is_uppercamelcase_string('')
    

def test_iotools_is_uppercamelcase_string_03():

    assert not iotools.is_uppercamelcase_string('fooBar')
    assert not iotools.is_uppercamelcase_string('foobar')
    assert not iotools.is_uppercamelcase_string('foo bar')
    assert not iotools.is_uppercamelcase_string('Foo Bar')
    assert not iotools.is_uppercamelcase_string('fb')
