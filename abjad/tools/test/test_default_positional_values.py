# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad.tools import *
pytest.skip()


@pytest.mark.parametrize('klass', documentationtools.list_all_abjad_classes())
def test_default_positional_values_01(klass):
    if '_storage_format' in dir(klass) and not inspect.isabstract(klass):
        instance = klass()
