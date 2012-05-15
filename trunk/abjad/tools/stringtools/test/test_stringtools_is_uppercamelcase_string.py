from abjad import *


def test_stringtools_is_uppercamelcase_string_01():

    assert stringtools.is_uppercamelcase_string('FooBar')
    assert stringtools.is_uppercamelcase_string('Foo')
    assert stringtools.is_uppercamelcase_string('FB')
    assert stringtools.is_uppercamelcase_string('F')


def test_stringtools_is_uppercamelcase_string_02():

    assert stringtools.is_uppercamelcase_string('')
    

def test_stringtools_is_uppercamelcase_string_03():

    assert not stringtools.is_uppercamelcase_string('fooBar')
    assert not stringtools.is_uppercamelcase_string('foobar')
    assert not stringtools.is_uppercamelcase_string('foo bar')
    assert not stringtools.is_uppercamelcase_string('Foo Bar')
    assert not stringtools.is_uppercamelcase_string('fb')
