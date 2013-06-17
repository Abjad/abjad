from abjad import *


def test_stringtools_is_lower_camel_case_string_01():

    assert stringtools.is_lower_camel_case_string('fooBar')
    assert stringtools.is_lower_camel_case_string('foo')
    assert stringtools.is_lower_camel_case_string('fB')
    assert stringtools.is_lower_camel_case_string('f')


def test_stringtools_is_lower_camel_case_string_02():

    assert stringtools.is_lower_camel_case_string('')


def test_stringtools_is_lower_camel_case_string_03():

    assert not stringtools.is_lower_camel_case_string('FooBar')
    assert not stringtools.is_lower_camel_case_string('Foobar')
    assert not stringtools.is_lower_camel_case_string('foo bar')
    assert not stringtools.is_lower_camel_case_string('Foo Bar')
