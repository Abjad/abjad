# -*- coding: utf-8 -*-
from abjad import *


def test_stringtools_is_snake_case_file_name_01():

    assert stringtools.is_snake_case_file_name('foo_bar.blah')
    assert stringtools.is_snake_case_file_name('foo.blah')
    assert stringtools.is_snake_case_file_name('foo_bar')
    assert stringtools.is_snake_case_file_name('foo')


def test_stringtools_is_snake_case_file_name_02():

    assert stringtools.is_snake_case_file_name('')


def test_stringtools_is_snake_case_file_name_03():

    assert not stringtools.is_snake_case_file_name('foo_bar.')
    assert not stringtools.is_snake_case_file_name('Foo_bar.blah')
    assert not stringtools.is_snake_case_file_name('foo_bar.Blah')
    assert not stringtools.is_snake_case_file_name('Foo_bar')
