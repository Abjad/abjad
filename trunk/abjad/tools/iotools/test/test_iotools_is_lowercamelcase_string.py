from abjad import *


def test_iotools_is_lowercamelcase_string_01():

    assert iotools.is_lowercamelcase_string('fooBar')
    assert iotools.is_lowercamelcase_string('foo')
    assert iotools.is_lowercamelcase_string('fB')
    assert iotools.is_lowercamelcase_string('f')


def test_iotools_is_lowercamelcase_string_02():

    assert iotools.is_lowercamelcase_string('')
    

def test_iotools_is_lowercamelcase_string_03():

    assert not iotools.is_lowercamelcase_string('FooBar')
    assert not iotools.is_lowercamelcase_string('Foobar')
    assert not iotools.is_lowercamelcase_string('foo bar')
    assert not iotools.is_lowercamelcase_string('Foo Bar')
