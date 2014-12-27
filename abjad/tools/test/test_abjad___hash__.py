# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad import *


ignored_classes = (
    datastructuretools.Enumeration,
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )
@pytest.mark.parametrize('class_', classes)
def test_abjad___hash___01(class_):
    r'''All concrete classes with __hash__ can hash.
    '''

    if not inspect.isabstract(class_):
        if getattr(class_, '__hash__', None):
            instance = class_()
            value = hash(instance)
            assert isinstance(value, int)