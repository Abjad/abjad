# -*- coding: utf-8 -*-
from abjad import *


def test_stringtools_is_snake_case_package_name_01():

    assert stringtools.is_snake_case_package_name('foo.bar.blah')
    assert stringtools.is_snake_case_package_name('foo.bar_blah')
    assert stringtools.is_snake_case_package_name('foo_bar.blah')
    assert stringtools.is_snake_case_package_name('foo')


def test_stringtools_is_snake_case_package_name_02():

    assert stringtools.is_snake_case_package_name('')


def test_stringtools_is_snake_case_package_name_03():

    assert not stringtools.is_snake_case_package_name('foo.bar.Blah')
    assert not stringtools.is_snake_case_package_name('foo.bar.BlahPackage')
    assert not stringtools.is_snake_case_package_name('Foo')
    assert not stringtools.is_snake_case_package_name('Foo.Bar')
