# -*- coding: utf-8 -*-
from abjad import *


def test_stringtools_is_lower_camel_case_01():

    assert stringtools.is_lower_camel_case('fooBar')
    assert stringtools.is_lower_camel_case('foo')
    assert stringtools.is_lower_camel_case('fB')
    assert stringtools.is_lower_camel_case('f')


def test_stringtools_is_lower_camel_case_02():

    assert stringtools.is_lower_camel_case('')


def test_stringtools_is_lower_camel_case_03():

    assert not stringtools.is_lower_camel_case('FooBar')
    assert not stringtools.is_lower_camel_case('Foobar')
    assert not stringtools.is_lower_camel_case('foo bar')
    assert not stringtools.is_lower_camel_case('Foo Bar')
