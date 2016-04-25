# -*- coding: utf-8 -*-
import inspect
import pytest
from abjad.tools import documentationtools


ignored_classes = (
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___rmul___01(class_):
    r'''All classes implementing __mul__ also implement __rmul__.
    '''
    if inspect.isabstract(class_):
        return
    if hasattr(class_, '__mul__'):
        assert hasattr(class_, '__rmul__')
