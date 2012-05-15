from abjad import *


def test_stringtools_is_lowercamelcase_string_01():

    assert stringtools.is_lowercamelcase_string('fooBar')
    assert stringtools.is_lowercamelcase_string('foo')
    assert stringtools.is_lowercamelcase_string('fB')
    assert stringtools.is_lowercamelcase_string('f')


def test_stringtools_is_lowercamelcase_string_02():

    assert stringtools.is_lowercamelcase_string('')
    

def test_stringtools_is_lowercamelcase_string_03():

    assert not stringtools.is_lowercamelcase_string('FooBar')
    assert not stringtools.is_lowercamelcase_string('Foobar')
    assert not stringtools.is_lowercamelcase_string('foo bar')
    assert not stringtools.is_lowercamelcase_string('Foo Bar')
