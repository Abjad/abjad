# -*- encoding: utf-8 -*-
from abjad import *


def test_stringtools_is_upper_camel_case_string_01():

    assert stringtools.is_upper_camel_case_string('FooBar')
    assert stringtools.is_upper_camel_case_string('Foo')
    assert stringtools.is_upper_camel_case_string('FB')
    assert stringtools.is_upper_camel_case_string('F')


def test_stringtools_is_upper_camel_case_string_02():

    assert stringtools.is_upper_camel_case_string('')


def test_stringtools_is_upper_camel_case_string_03():

    assert not stringtools.is_upper_camel_case_string('fooBar')
    assert not stringtools.is_upper_camel_case_string('foobar')
    assert not stringtools.is_upper_camel_case_string('foo bar')
    assert not stringtools.is_upper_camel_case_string('Foo Bar')
    assert not stringtools.is_upper_camel_case_string('fb')
