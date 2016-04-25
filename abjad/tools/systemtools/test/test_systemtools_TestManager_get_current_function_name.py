# -*- coding: utf-8 -*-
from abjad import *


def test_systemtools_TestManager_get_current_function_name_01():

    def bar():
        return systemtools.TestManager.get_current_function_name()

    assert bar() == 'bar'


def test_systemtools_TestManager_get_current_function_name_02():

    def foo():
        return systemtools.TestManager.get_current_function_name()

    assert foo() == 'foo'
