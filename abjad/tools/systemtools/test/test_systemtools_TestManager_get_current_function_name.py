# -*- coding: utf-8 -*-
import abjad
from abjad.tools import systemtools


def test_systemtools_TestManager_get_current_function_name_01():

    def bar():
        return systemtools.TestManager.get_current_function_name()

    assert bar() == 'bar'


def test_systemtools_TestManager_get_current_function_name_02():

    def foo():
        return systemtools.TestManager.get_current_function_name()

    assert foo() == 'foo'
