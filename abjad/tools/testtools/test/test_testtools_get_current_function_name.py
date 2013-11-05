# -*- encoding: utf-8 -*-
from abjad import *


def test_testtools_get_current_function_name_01():

    def bar():
        return testtools.get_current_function_name()

    assert bar() == 'bar'


def test_testtools_get_current_function_name_02():

    def foo():
        return testtools.get_current_function_name()

    assert foo() == 'foo'
