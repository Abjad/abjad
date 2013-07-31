# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import introspectiontools


def test_introspectiontools_get_current_function_name_01():

    def bar():
        return introspectiontools.get_current_function_name()

    assert bar() == 'bar'


def test_introspectiontools_get_current_function_name_02():

    def foo():
        return introspectiontools.get_current_function_name()

    assert foo() == 'foo'
