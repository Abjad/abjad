# -*- coding: utf-8 -*-
from abjad import *


def test_stringtools_is_upper_camel_case_01():

    assert stringtools.is_upper_camel_case('FooBar')
    assert stringtools.is_upper_camel_case('Foo')
    assert stringtools.is_upper_camel_case('FB')
    assert stringtools.is_upper_camel_case('F')


def test_stringtools_is_upper_camel_case_02():

    assert stringtools.is_upper_camel_case('')


def test_stringtools_is_upper_camel_case_03():

    assert not stringtools.is_upper_camel_case('fooBar')
    assert not stringtools.is_upper_camel_case('foobar')
    assert not stringtools.is_upper_camel_case('foo bar')
    assert not stringtools.is_upper_camel_case('Foo Bar')
    assert not stringtools.is_upper_camel_case('fb')
