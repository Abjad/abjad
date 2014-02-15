# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad.tools import documentationtools


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___hash___01(class_):
    r'''All concrete classes with __hash__ can hash.
    '''

    if not inspect.isabstract(class_):
        if hasattr(class_, '__hash__'):
            instance = class_()
            value = hash(instance)
            assert isinstance(value, int)
